#!/usr/bin/env python3
"""
    watchdog.py - A watchdog service for the device manager. Sends heartbeats to every
            other component in the system and informs their status to the device manager.
            Each instance of watchdog manages health checkups of up to 10 components.
    Author: mgmt
    Date: 11/30/2017
"""
from threading import Thread
import requests
import time

class WatchDog(Thread):
    def __init__(self, dm, hosts):
        """
            :param dm: host url of device_manager
            :param hosts: a list of hosts to ping for a watchdog
        """
        Thread.__init__(self)
        self.dm = dm
        self.hosts = hosts

    def send_heartbeats(self):
        dm_url = 'http://{0}/{1}/'.format(self.dm,'set_health')
        while (len(self.hosts) > 0):
            for host in self.hosts['host']:
                comp_url = 'http://{0}/{1}/'.format(host,'get_health')
                try:
                    r = requests.get(url)   # hit get_health endpoint on every component
                                            # returns {'health':status}
                    message = requests.post(dm_url, json={'host':host,
                                                          'health':r['health']})
                except:
                    print('error connecting to host...')
            time.delay(30)

    def run(self):
        self.send_heartbeats()
