"""
    Wrapper for the managment teams queue endpoints.
    Nov, 27, 2017 - Matt Jones matthewjones@bennington.edu
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

        links = resp.json()['links']
        if 'chunk_id' in resp.json():
            c_id = resp.json()['chunk_id']
        else:
            c_id = None

        return (links, c_id)

    # TODO: remove this, no longer implemmented in mgmt
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

        links = resp.json()['links']
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
                json={'links' : links}
                )

        return resp.status_code in [200, 201]
