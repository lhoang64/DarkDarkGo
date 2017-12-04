"""
    Main crawling module, pulls links from the mgmt queue, and crawls them.
    Nov, 28, 2017 - Matt Jones matthewjones@bennington.edu
"""
import logging
from multiprocessing import Pool
from threading import Event
from time import sleep

from spider.spider import Spider
from mgmt.queue import QueueWrapper
from mgmt.device_manager import DeviceManager
from util.util import get_tor_session


class Crawler:
    def __init__(
            self,
            num_threads, # Number of thread with which to crawl.
            user_agent,  # User agent to include in requeset.
            queue_host,
            dm_host
            ):
        """
        This instantiates the crawler. We alert the DM that we are online,
            and wait for `run()` to be called.

        Both host params are accepted in the form of a namedtuple, with `ip`
            and `port` fields.
        """
        self.num_threads = num_threads
        self.user_agent  = user_agent
        self._queue      = QueueWrapper(queue_host)
        self._manager    = DeviceManager(dm_host)

        self.chunk_id    = ''
        self.log = logging.getLogger()
        self.running = Event() # TODO Maybe wrap this?

        if not self._declare_online():
            raise ConnectionError("Couldn't connect to the device manager.")
        # TODO Create and start managment thread.

    def _declare_online(self):
        """
        Sends management a request saying that we are online.
        """
        return self._manager.alert_online()

    def _add_to_chunk(self, link, html):
        # TODO Impliment this once Linh makes the API available.
        pass

    def _crawl_link(self, link):
        spider = Spider(
                link,
                self.user_agent,
                get_tor_session()
                )
        spider.crawl()
        if spider.success:
            self._add_to_chunk(
                    link,
                    spider.html
                    )
            self._manager.mark_link_crawled(link)
            return spider.links
        else:
            self._manager.mark_link_crawled(link)
            return []

    def stop(self):
        """
        Tells the thread to stop looping until start() is called.
        """
        self.running.clear()

    def re_start(self):
        """
        Tells the thread that it should be running.
        """
        self.running.set()

    def is_running(self):
        return self.running.is_set()

    def get_chunks(self):
        """
        Method to return a list of chunks stored on the crawler, lists all
            chunks stored, including WIP chunks.

        Returns: [chunk_id]
        """
        # TODO Impliment this.
        pass

    def run(self):
        # TODO Find a more robust way of starting/stopping and keeping track.
        while self.running.wait():
            links, chunk_id = self._manager.get_links()
            self.chunk_id = chunk_id
            if not links:
                self.running.clear()
                self.running.wait(60)
                self.running.set()
                continue

            # TODO Throttle this somehow.
            pool = Pool(self.num_threads)
            link_multilist = pool(self._crawl_link, links)
            # The following line is an affront to god.
            fresh_links = [link for sublist in mulit_list for link in sublist]
            self._queue.add_links(fresh_links)
            self._manager.alert_chunk(chunk_id)
