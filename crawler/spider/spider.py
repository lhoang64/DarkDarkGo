"""
    This is a spider; it is a seperate class from the crawler because here
        we can cleanly encapsulate all the real scrapign logic.
    Nov, 28, 2017 - Matt Jones matthewjones@bennington.edu
"""
import re
import logging

from bs4 import BeautifulSoup
from requests import exceptions


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
        self.spider_err  = False
        self.body        = ''
        self.title       = ''
        self.links       = []

        self.log = logging.getLogger()

    def crawl(self):
        """
        Request the link, scrapes for hrefs. Stores status code/MIME type/html
            is respective object variables.

        Returns: nothing
        """
        self.log.info('crawling link: {}'.format(self.link))
        try:
            resp = self.session.get(
                    self.link,
                    headers={'User-Agent': self.user_agent}
                    )
        except ConnectionError as conn_err:
            # TODO What should we do here?
            self.log.exception('What?')
            self.spider_err = True
            return
        except exceptions.Timeout as to_err:
            self.log.warning(
                    'Request to {} timed out, marking as dead.'
                    .format(self.link)
                    )
            self._dead_link()
            return
        except exceptions.RequestException as req_err:
            self.log.exception(
                    'Hit internal requests error, failed to spider {}'
                    .format(self.link)
                    )
            self.spider_err = True
            return

        self.log.info('successfully connected to {}'.format(self.link))
        self.body = resp.text
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title
        self._find_links(soup)

        self.log.info('Successfully spidered {}'.format(self.link))
        self.log.debug('Found {} links.'.format(len(self.links)))

    def _dead_link(self, status_code=None):
        self.status_code = status_code
        self.success = False

    def _find_links(self, soup):
        for elem in soup.find_all('a', href=True):
            link = elem['href']
            self._add_link(link)

    def _add_link(self, link):
        absolute_url_re = re.compile(
                '^(http|https):\/\/[A-Za-z0-9]*.onion\/[A-Za-z0-9\/\-._]*'
                )
        relative_url_re = re.compile(
                '^\/[A-Za-z0-9\/\-._]*'
                )
        abs_url = absolute_url_re.match(link)
        if abs_url:
            self.links.append(abs_url.group())
        else:
            rel_url = relative_url_re.match(link)
            if rel_url:
                self.links.append(rel_url.group())
