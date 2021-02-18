import logging
import uuid
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from aggregator.data_platform.utils.auditable_etl import AuditableEtl


class Scraper(AuditableEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, destination_extension='csv')

    def extract(self, source):

        data = []

        for url_id, url, source_site in source:
            response = requests.get(url)
            page = response.text
            data += [(url_id, source_site, page)]

            logging.info(f'{self.process_name} {url}')

        data = pd.DataFrame(data, columns=['url_id', 'source', 'html'])

        return data

    def transform(self, data: pd.DataFrame):
        data['html'] = data['html'].map(self.get_body)
        return data

    def load(self, data: pd.DataFrame, destination: str):

        data = data.groupby('source')

        for source, pages in data:
            path = destination.format(source)
            Path(path).parent.mkdir(exist_ok=True)
            pages = pages[['url_id', 'html']]
            pages.to_csv(path, index=False)

    def start_audit(self, source, destination: str):

        query = []
        for url_id, url, source_site in source:
            path_destination = destination.format(source_site)
            query += [f"('{url_id}','{path_destination}','{self.process_name}')"]

        query = ','.join(query)
        query = f"insert into url_audit (url_id, destination, process_name) values {query} returning id;"

        self.cursor.execute(query)
        audit_ids = self.cursor.fetchall()

        return audit_ids

    def stop_audit(self, audit_ids):

        audit_ids = [str(_[0]) for _ in audit_ids]
        audit_ids = ','.join(audit_ids)
        audit_ids = f'({audit_ids})'

        query = f'update url_audit set stop_time = now() where id in {audit_ids};'
        self.cursor.execute(query)

    def get_unprocessed_source(self):
        query = f"select * from get_unprocessed_urls('{self.process_name}');"
        self.cursor.execute(query)
        return self.cursor.fetchall()  # todo limit 5000

    def get_destination(self):
        return f'{self.path_destination.as_posix()}/{{}}/{uuid.uuid1()}.{self.destination_extension}'

    def get_body(self, page: str):
        soup = BeautifulSoup(page, 'html.parser')
        body = str(soup.body)
        return body
