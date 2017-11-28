"""
    Wrapper for the managment teams queue endpoints.
    Nov, 27, 2017 - Matt Jones matthewjones@bennington.edu

    NOTE: For now, this doesn't actually interact with the queue server,
        it's just a dummy until the server is up.
"""

class QueueWrapper:

    def __init__(self, queue_host):
        self._address = queue_host.ip
        self._port = queue_host.port

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

        links = ['https://zqktlwi4fecvo6ri.onion']
        c_id = 0

        return (links, c_id)

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
        pass
