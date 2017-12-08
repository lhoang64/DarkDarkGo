"""
    Wrapper for the managment teams queue endpoints.
    Nov, 27, 2017 - Matt Jones matthewjones@bennington.edu

    NOTE: For now, this doesn't actually interact with the queue server,
        it's just a dummy until the server is up.
"""

import requests
import logging

class QueueWrapper:

    def __init__(self, queue_host):
        self._address = queue_host.ip
        self._port = queue_host.port

        self.log = logging.getLogger()

    def get_links(self):
        """
        The `/get_links` endpoint returns n links, as well as a new chunk id.
        Returns a tuple of (list of links, chunk id)

        Response JSON should look like:
        {
            "links" : [string],
            "chunk_id" : string
        }
        """
        self.log.debug('Requesting new chunk/links from management.')

        resp = requests.get(
                'http://{}:{}/get_links'.format(self._address, self._port)
                )

        links = resp.json['links']
        c_id = resp.json['chunk_id']

        return (links, c_id)

    def get_n_links(self, n_links):
        """
        Requests n more links from the queue. This should only be used to fill
            in for failed links.

        Response JSON should look like:
        {
            "links": ["stuff_1.onion", "stuff_2.onion", "stuff_3.onion"]
        }

        Returns: a list of strings, each an onion link.
        """
        resp = requests.get(
                'http://{}:{}/get_links/{}'.format(
                    self._address,
                    self._port,
                    n_links
                    )
                )

        links = resp.json['links']
        self.log.info(
                'Requested {} more links from management, received {}.'
                .format(n_links, len(links))
                )

        return links

    def add_links(self, links):
        """
        The `/add_links` endpoint adds links to the queue (if they are not
            already handled).
        prarm: links : A list of strings, where each sring is a .onion url.

        Request JSON should look like:
        {
            "links" : [string]
        }
        """

        self.log.info(
                'Adding {} links to management\'s queue'
                .format(len(links))
                )

        resp = requests.post(
                'http://{}:{}/add_links'.format(
                    self._address,
                    self._port
                    ),
                data={'links' : links}
                )

        return resp.status_code == 200
