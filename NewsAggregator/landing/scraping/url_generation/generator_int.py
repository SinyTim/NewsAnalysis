import requests
import pandas as pd

from landing.scraping.url_generation.generator import UrlGenerator


class UrlGeneratorWithIntState(UrlGenerator):

    def __init__(self, max_n_fails: int, **kwargs):
        super().__init__(**kwargs)

        self.max_n_fails = max_n_fails

    def _generate(self, start_state):

        page_index = start_state
        last_success_page_index = None
        n_fails = 0

        urls = []
        urls_bad = []

        while n_fails < self.max_n_fails:

            url = self._get_urls_from_state(page_index)

            response = requests.get(url)

            if (response.status_code == 200) and (response.url != 'https://news.tut.by/'):
                urls += [(url, response.url)]
                n_fails = 0
                last_success_page_index = page_index
            else:
                urls_bad += [(url, response.url, response.status_code)]
                n_fails += 1

            page_index = self._increment_state(page_index)

        urls = pd.DataFrame(urls, columns=['url', 'url_response'])
        urls_bad = pd.DataFrame(urls_bad, columns=['url', 'url_response', 'status_code'])

        stop_state = last_success_page_index + 1 if last_success_page_index else start_state

        return urls['url_response'], urls_bad, stop_state

    def _state_from_str(self, state: str):
        return int(state)

    def _state_to_str(self, state):
        return str(state)

    def _get_urls_from_state(self, state):
        state = self._state_to_str(state)
        url = self.url_template.format(state)
        return url

    def _increment_state(self, state):
        return state + 1
