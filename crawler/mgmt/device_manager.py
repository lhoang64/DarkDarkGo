"""
    Wrapper for the managment teams device manager endpoints.
    Nov, 27, 2017 - Matt Jones matthewjones@bennington.edu
"""

import requests
import logging

class DeviceManager:

    def __init__(self, dm_host):
        self._address = dm_host.ip
        self._port = dm_host.port

        self.log = logging.getLogger()

    def _set_state(self, state):
        self.log.info('Setting state to {}'.format(state))
        try:
            url_str = 'http://{}:{}/set_state/component'.format(
                    self._address,
                    self._port
                    )
            self.log.debug(url_str)
            resp = requests.post(url_str, json={'state' : state})
            return resp.status_code in [200, 201]
        except:
            self.log.exception('Failed to set state.')
            return False

    def alert_online(self):
        """
        The Device manager needs to know that the crawler has started.
        This method sends an alert to the DM, sayign that we are online.

        TODO: Get request format from mgmt team.
        """
        return self._set_state('online')

    def send_waiting(self):
        """
        In the event that there are no new seeds, we need to tell the DM that
            we are waiting.

        TODO: Get request format from mgmt team.
        """
        return self._set_state('waiting')

    def send_error(self):
        """
        Tell the mgmt team that we hit a fatal error, and that we won't
            continue to run.

        Note: Does not take any params.
        """
        return self._set_state('error')

    def get_unprop_chunks(self):
        """
        Requests the list of chunks which should be stored on the crawler.

        Response JSON should look like:
        {
            "chunks": [100, 101, 102]
        }
        """
        resp = requests.get(
                'http://{}:{}/get_chunks/unpropagated'.format(
                    self._address,
                    self._port
                    )
                )

        chunks = resp.json()['chunks']

        return chunks

    def alert_chunk(self, chunk_id):
        """
        Alerts mgmt that we are done this the chunk corresponding to chunk_id.

        param: chunk_id : String corresponding to the id of the chunk we just
            finished.
        param: address  : Named Tuple containing our ip and the port to
            contact us on.

        format should be:
        {
            "chunk_id": 101,
            "state": "crawled"
        }
        """
        resp = requests.post(
                'http://{}:{}/set_state/content_chunk'.format(
                    self._address,
                    self._port
                    ),
                json={
                    'chunk_id' : chunk_id,
                    'state'    : 'crawled'
                    }
                )
        return resp.status_code in [200, 201]

    def mark_link_crawled(self,link, success):
        """
        Alert's management that `link` has been crawled, and does not need to
            be checked again. Uses the /add_crawled_link endpoint.

        param: link : String containing the link which has been crawled.
        """
        if success:
            state = 'crawled'
        else:
            state = 'error'
        resp = requests.post(
                'http://{}:{}/set_state/link'.format( # formerly crawler
                    self._address,
                    self._port
                    ),
                json={'link' : link, 'state' : state}
                )