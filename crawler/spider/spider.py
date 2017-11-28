"""
    This is a spider; it is a seperate class from the crawler because here
        we can cleanly encapsulate all the real scrapign logic.
    Nov, 28, 2017 - Matt Jones matthewjones@bennington.edu
"""

from bs4 import BeautifulSoup


class Spider:
    def __init__(
            self,
            link,
            user_agent,
            session
            ):
        self.link        = link
        self.user_agent  = user_agent
        self.session     = session
        self.status_code = None
        self.success     = None
        self.body        = ''
        self.links       = []

    def crawl(self):
        """
        Request the link, scrapes for hrefs. Stores status code/MIME type/html
            is respective object variables.

        Returns: nothing
        """
        # TODO Implement this.

    def _find_links(html):
        pass
