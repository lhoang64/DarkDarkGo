#!/usr/bin/env python3
"""
    watchdog.py - A watchdog service for the device manager. Sends heartbeats to every
            other component in the system and informs their status to the device manager.
            Each instance of watchdog manages health checkups of up to 10 components.
    Author: mgmt
    Date: 11/30/2017
"""
from threading import Thread
from database_manager import DatabaseManager
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
        dm_url = 'http://{0}/{1}/'.format(self.dm,'set_health')
        while (len(self.hosts) > 0):
            for host in self.hosts:
                component_url = 'http://{0}/{1}/'.format(host,'get_health')
                try:
                    r = requests.get(component_url)     # hit get_health endpoint on every component
                                                        # returns {'health':health_status}
                    requests.post(dm_url,json={'host':host,'health':r['health']})
                except:
                    print('error connecting to host...')
                time.sleep(2)
            time.sleep(30)

    def run(self):
        print('running thread {0}'.format(self.thread_id))
        for host in self.hosts:
            print('Watchdog {0} sending heartbeats to {1}'.format(self.thread_id, host))
        self.send_heartbeats()

def main():
    wd_num_items = 10
    thread_count = 0
    dm = '0.0.0.0:5000'
    db_manager = DatabaseManager()
    host_relation = db_manager.get_relation('host')

    j = 0
    watchdogs = []
    hosts = []
    for i in range(0,len(host_relation)):
        if j < wd_num_items:
            hosts.append(host_relation[i]['host'])
            j += 1
            if j >= wd_num_items:
                thread_count += 1
                wd = WatchDog(thread_count, dm, hosts)
                watchdogs.append(wd)
                hosts = []
                j = 0

    if (wd_num_items > len(hosts) > 0):
        thread_count += 1
        wd = WatchDog(thread_count, dm, hosts)
        watchdogs.append(wd)

    for wd in watchdogs:
        wd.start()



if __name__ == "__main__":
    print('running application...')
    main()