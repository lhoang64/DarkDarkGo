"""
    Wrapper for the managment teams device manager endpoints.
    Nov, 27, 2017 - Matt Jones matthewjones@bennington.edu

    NOTE: For now, this doesn't actually interact with the DM server,
        it's just a dummy until the server is up.
"""

import requests

class DeviceManager:

    def __init__(self, dm_host):
        self._address = dm_host.ip
        self._port = dm_host.port

    def _set_state(self, state):
        try:
            resp = requests.post(
                    self._address + '/set_state/component',
                    data={'state' : state}
                    )
            return resp.status_code == 200
        except:
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

    def get_chunks(self):
        """
        Requests the list of chunks which should be stored on the crawler.

        Response JSON should look like:
        [int]
        """
        chunks = [1, 2, 3]

        return chunks

    def alert_chunk(chunk_id, address):
        """
        Alerts mgmt that we are done this the chunk corresponding to chunk_id.

        param: chunk_id : String corresponding to the id of the chunk we just
            finished.
        param: address  : Named Tuple containing our ip and the port to
            contact us on.
        """
        pass

    def mark_link_crawled(link, success):
        """
        Alert's management that `link` has been crawled, and does not need to
            be checked again. Uses the /add_crawled_link endpoint.

        param: link : String containing the link which has been crawled.
        """
        if success:
            state = 'crawled'
        else:
            state = 'error'
        requests.post(
                self._address + '/set_state/link',
                data={'link' : link, 'state' : state}
                )
