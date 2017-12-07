"""
    Main crawling module, pulls links from the mgmt queue, and crawls them.
    Nov, 28, 2017 - Matt Jones matthewjones@bennington.edu
"""
import logging
import os
from multiprocessing import Pool
from threading import Event
from time import sleep

from spider.spider import Spider
from mgmt.queue import QueueWrapper
from mgmt.device_manager import DeviceManager
from util.util import get_tor_session
from chunk import Chunk


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
        self.chunk       = None
        self.log = logging.getLogger()
        self.running = Event() # TODO Maybe wrap this?

        if self._declare_online():
            self.log.info('Crawler initialized successfully!')
        else:
            raise ConnectionError("Couldn't connect to the device manager.")

    def _declare_online(self):
        """
        Sends management a request saying that we are online.
        """
        return self._manager.alert_online()

    def _create_chunk(self):
        """
        Instantiate chunk object for crawler to use to create headers and documents. Create chunk file to be writen to.
        :return: Chunk object
        """
        self.chunk = Chunk(self.chunk_id)
        self.chunk.create_chunk()
        return self.chunk

    def _create_document(self, link, html, title):
        """
        Used by spiders crawling and scraping links to create documents to be added to chunk
        :param link: string
        :param html: string
        :param title: string
        :return: none
        """
        self.chunk.compute_file_header_value(len(self.chunk.header))
        self.chunk.create_document(link, html, title)

    def _add_to_chunk(self):
        """
        Called when all spiders done crawling links in that session(5 links). Write all documents to chunks.
        Then write header(footer) to chunk.
        :return: none
        """
        self.chunk.append_to_chunk()
        self.chunk.append_header_to_chunk()

    def _crawl_link(self, link):
        spider = Spider(
                link,
                self.user_agent,
                get_tor_session()
                )
        spider.crawl()
        self._manager.mark_link_crawled(link, spider.success)
        if spider.success:
            self._create_document(
                    link,
                    spider.html,
                    spider.title
                    )
            return spider.links
        else:
            return []

    def stop(self):
        """
        Tells the thread to stop looping until start() is called.
        """
        self.log.warning('Crawler going to stand-by.')
        self.running.clear()

    def re_start(self):
        """
        Tells the thread that it should be running.
        """
        self.log.warning('Crawler resuming.')
        self.running.set()

    def is_running(self):
        return self.running.is_set()

    def get_chunks(self):
        """
        Called on a crawler instance, Method to return a list of chunks stored on the crawler, lists all
            chunks stored, including WIP chunks.
        """
        path = '/data'
        chunks = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return chunks

    def run(self):
        # TODO Find a more robust way of starting/stopping and keeping track.
        while self.running.wait():
            links, chunk_id = self._manager.get_links()
            self.log.info('starting new chunk: {}'.format(chunk_id))
            self.chunk_id = chunk_id
            self._create_chunk()  # create chunk object when crawler starts
            if not links:
                self.log.warning(
                        "Didn't get any links from management, waiting for 60."
                        )
                self.running.clear()
                self.running.wait(60)
                self.running.set()
                self.log.warning('Resuming crawler.')
                continue

            # TODO Throttle this somehow.
            pool = Pool(self.num_threads)
            link_multilist = pool(self._crawl_link, links)
            # The following line is an affront to god.
            fresh_links = [link for sublist in mulit_list for link in sublist]
            self._queue.add_links(fresh_links)
            # Linh - i'm assuming that by this point all spiders have finished crawling the links provided by mgmt
            #        write all documents to chunk
            self._add_to_chunk()
            self._manager.alert_chunk(chunk_id)
