import uuid
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path

from utils.auditable_etl import AuditableEtl


class Scraper(AuditableEtl):

    def __init__(self, process_name: str, path_destination: Path):
        super().__init__()

        self.process_name = process_name
        self.path_destination = path_destination

    def extract(self, source):

        data = []

        for url_id, url, source_cite in source:
            response = requests.get(url)
            page = response.text
            data += [(url_id, source_cite, page)]

        data = pd.DataFrame(data, columns=['url_id', 'source', 'html'])

        return data

    def transform(self, data):
        data['html'] = data['html'].map(self.get_body)
        return data

    def load(self, data, destination):

        data = data.groupby('source')

        for source, pages in data:
            path = destination.format(source)
            pages = pages[['url_id', 'html']]
            pages.to_csv(path, index=False)

    def start_audit(self, source, destination):

        query = []
        for url_id, url, source_cite in source:
            path_destination = destination.format(source_cite)
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
        return self.cursor.fetchall()

    def get_destination(self):
        return f'{self.path_destination.as_posix()}/{{}}/{uuid.uuid1()}.csv'

    def get_body(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        body = str(soup.body)
        return body
