#! /usr/bin/env python3
"""
    watchdog.py - A watchdog service for the device manager. Sends heartbeats to every
            other component in the system and informs their status to the device manager.
            Each instance of watchdog manages health checkups of up to 10 components.
    Author: Nidesh Chitrakar (nideshchitrakar@bennington.edu)
    Date: 11/30/2017
"""
from threading import Thread
from database_manager import DatabaseManager
from constants import number_of_comps
import requests
import time


class WatchDog(Thread):
    def __init__(self, thread_id, dm, hosts):
        """
        :param dm: host url of device_manager
        :param hosts: a list of hosts to ping for a watchdog
        """
        Thread.__init__(self)
        self.thread_id = thread_id
        self.dm = dm
        self.hosts = hosts

    def send_heartbeats(self):
        dm_url = 'http://{0}/{1}'.format(self.dm, 'set_health')
        while len(self.hosts) > 0:
            for host in self.hosts:
                component_url = 'http://{0}:5000/{1}'.format(host, 'get_health')
                try:
                    r = requests.get(component_url)     # hit get_health endpoint on every component
                                                        # returns {'status':health_status}
                    requests.post(dm_url, json={'host': host,
                                                'status': r['status'],
                                                'state': 'online'})
                except:
                    print('wd{0}: error connecting to host {1}'.format(self.thread_id, host))
                    requests.post(dm_url, json={'host': host,
                                                'status': 'error',
                                                'state': 'offline'})
                time.sleep(2)
            time.sleep(30)

    def run(self):
        for host in self.hosts:
            print('Watchdog {0} sending heartbeats to {1}'.format(self.thread_id, host))
        self.send_heartbeats()


def main():
    thread_count = 0
    dm = '0.0.0.0:5000'
    db_manager = DatabaseManager()
    host_relation = db_manager.get_relation('host')

    j = 0
    watchdogs = []
    hosts = []
    for i in range(0, len(host_relation)):
        if j < number_of_comps:
            hosts.append(host_relation[i]['host'])
            j += 1
            if j >= number_of_comps:
                thread_count += 1
                wd = WatchDog(thread_count, dm, hosts)
                watchdogs.append(wd)
                hosts = []
                j = 0

    if number_of_comps > len(hosts) > 0:
        thread_count += 1
        wd = WatchDog(thread_count, dm, hosts)
        watchdogs.append(wd)

    for wd in watchdogs:
        wd.start()


if __name__ == "__main__":
    print('running watchdog...')
    main()
