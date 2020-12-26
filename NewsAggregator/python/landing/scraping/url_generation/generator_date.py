import datetime
import urllib.parse

import pandas as pd
import requests
from bs4 import BeautifulSoup

from landing.scraping.url_generation.generator import UrlGenerator


class UrlGeneratorWithDateState(UrlGenerator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.last_page_html_tag = 'li'
        self.last_page_html_class = 'pager-last'
        self.link_html_tag = 'h3'
        self.link_html_class = 'media-heading'
        self.url_param_page = 'page'
        self.url_base = 'https://naviny.media'

    def generate(self, start_state):

        urls = []
        urls_bad = []

        state = start_state
        date_today = datetime.date.today()

        while state < date_today:

            url = self.get_url_with_state(state)
            response = requests.get(url)

            if response.status_code == 200:
                page = response.text
                soup = BeautifulSoup(page, 'html.parser')

                link_last_page = soup.find_all(self.last_page_html_tag, class_=self.last_page_html_class)[0]
                url_last_page = link_last_page.findChildren('a', recursive=False)[0]['href']
                url_last_page = urllib.parse.urlparse(url_last_page)
                index_last_page = urllib.parse.parse_qs(url_last_page.query)[self.url_param_page]
                index_last_page = int(index_last_page[0])

                for index_page in range(index_last_page + 1):

                    url_page = f'{url}?{self.url_param_page}={index_page}'
                    response = requests.get(url_page)

                    if response.status_code == 200:
                        page = response.text
                        soup = BeautifulSoup(page, 'html.parser')
                        links = soup.find_all(self.link_html_tag, class_=self.link_html_class)
                        urls_current = [link.findChildren('a', recursive=False)[0]['href'] for link in links]
                        urls_current = [f'{self.url_base}{url_current}' for url_current in urls_current]
                        urls += urls_current
                    else:
                        urls_bad += [(url_page, response.url, response.status_code)]

            else:
                urls_bad += [(url, response.url, response.status_code)]

            state = self.increment_state(state)

        urls = pd.Series(urls)
        urls_bad = pd.DataFrame(urls_bad, columns=['url', 'url_response', 'status_code'])
        stop_state = state

        return urls, urls_bad, stop_state

    def state_from_str(self, state: str):

        year, month, day = state.split('/')

        year = int(year)
        month = int(month)
        day = int(day)

        state = datetime.date(year, month, day)

        return state

    def state_to_str(self, state):

        year = state.year
        month = state.month
        day = state.day

        state = f'{year}/{month}/{day}'

        return state

    def get_url_with_state(self, state):
        state = self.state_to_str(state)
        url = self.url_template.format(state)
        return url

    def increment_state(self, state):
        return state + datetime.timedelta(days=1)
