"""
    Just a file to store helper functions which would otherwise clutter
        up other modules.
    Nov, 27, 2017 - Matt Jones matthewjones@bennington.edu
"""
import requests
from collections import namedtuple

Host = namedtuple('Host', 'ip port')


def get_tor_session(port):
    """
    The python requests lib does not work nativly with tor, so we need to
        tell it to connect to the tor proxy.

    Heavily influenced by: https://stackoverflow.com/a/33875657/5843840

    param: port : port which tor is listening on (often 9050, 9051, or 9151)
    returns: a requests.session object.
    """
    proxies = {
            'http': 'socks5h://127.0.0.1:{}'.format(port)
            }

    session = requests.Session()
    session.proxies = proxies

    return session


def get_requests_session():
    """
    Like `get_tor_session`, but it's the clear-net. This should only be used
        to connect to the management servers.

    returns: a requests.session object.
    """
    session = requests.Session()

    return session
