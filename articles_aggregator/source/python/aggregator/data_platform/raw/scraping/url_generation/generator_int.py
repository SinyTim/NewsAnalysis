import logging

import pandas as pd
import requests

from aggregator.data_platform.raw.scraping.url_generation.generator import UrlGenerator


class UrlGeneratorWithIntState(UrlGenerator):

    def __init__(self, max_n_fails: int, **kwargs):
        super().__init__(**kwargs)

        logging.basicConfig(level=logging.INFO)

        self.max_n_fails = max_n_fails
        self.bad_response_url = 'https://news.tut.by/'

    def generate(self, start_state):

        page_index = start_state
        last_success_page_index = None
        n_fails = 0

        urls = []
        urls_bad = []

        while n_fails < self.max_n_fails:

            url = self.get_url_with_state(page_index)

            response = requests.get(url)

            if (response.status_code == 200) and (response.url != self.bad_response_url):
                urls += [response.url]
                n_fails = 0
                last_success_page_index = page_index
            else:
                urls_bad += [(url, response.url, response.status_code)]
                n_fails += 1

            page_index = self.increment_state(page_index)

            logging.info(f'{self.process_name} {url}')

        urls = pd.DataFrame(urls, columns=['url'])
        urls_bad = pd.DataFrame(urls_bad, columns=['url', 'url_response', 'status_code'])

        stop_state = self.increment_state(last_success_page_index) if last_success_page_index else start_state

        return urls, urls_bad, stop_state

    def state_from_str(self, state: str):
        return int(state)

    def state_to_str(self, state):
        return str(state)

    def get_url_with_state(self, state):
        state = self.state_to_str(state)
        url = self.url_template.format(state)
        return url

    def increment_state(self, state):
        return state + 1
