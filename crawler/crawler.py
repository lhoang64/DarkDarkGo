"""
    Main crawling module, pulls links from the mgmt queue, and crawls them.
    Nov, 28, 2017 - Matt Jones matthewjones@bennington.edu
"""
import logging
from multiprocessing import Pool
from time import sleep

from spider import Spider
from mgmt import QueueWrapper, DeviceManager
from util import get_tor_session


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

        self.running     = True
        self.waiting     = False
        self.chunk_id    = ''
        self.log = logging.getLogger()

        self._declare_online()
        # TODO Create and start managment thread.

    def _declare_online(self):
        self._manager.alert_online()
        # TODO This may return something? We may need to do something with it.

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

    def run(self):
        self.running = True
        while self.running:
            links, chunk_id = self._manager.get_links()
            self.chunk_id = chunk_id
            if not links:
                self.running = True
                sleep(60)

            # TODO Throttle this somehow.
            pool = Pool(self.num_threads)
            link_multilist = pool(self._crawl_link, links)
            # The following line is an affront to god.
            fresh_links = [link for sublist in mulit_list for link in sublist]
            self._queue.add_links(fresh_links)
            self._manager.alert_chunk(chunk_id)
