from pathlib import Path
import pandas as pd
import uuid

from utils.auditable_etl import AuditableEtl


class StagingHtmlEtl(AuditableEtl):

    def __init__(self, process_name: str, columns, path_source: Path, path_destination: Path):
        super().__init__()

        self.columns = columns
        self.process_name = process_name
        self.path_source = path_source
        self.path_destination = path_destination

        self.path_destination.mkdir(exist_ok=True)

    def parse_html(self, html):
        raise NotImplementedError

    def extract(self, source):
        data = [pd.read_csv(path_file) for path_file in source]
        data = pd.concat(data, ignore_index=True)
        return data

    def transform(self, data):
        parsed_data = data['html'].map(self.parse_html)

        bad_data = parsed_data[parsed_data.map(type) == str]
        bad_data = pd.concat((data['url_id'].loc[bad_data.index], bad_data), axis=1)
        bad_data.columns = ['url_id', 'error']

        parsed_data = parsed_data.apply(pd.Series)
        parsed_data.columns = self.columns
        data = pd.concat((data, parsed_data), axis=1)
        data = data.drop('html', axis=1)
        data = data.drop(bad_data.index)

        return data, bad_data

    def load(self, data, destination):
        data, bad_data = data

        data.to_csv(destination, index=False)

        if len(bad_data) != 0:
            self.write_bad_data(bad_data)

    def start_audit(self, source, destination):

        query = []
        for path_source in source:
            query += [f"('{path_source}','{destination}','{self.process_name}')"]

        query = ','.join(query)
        query = f"insert into audit (source, destination, process_name) values {query} returning id;"
        self.cursor.execute(query)
        audit_ids = self.cursor.fetchall()

        return audit_ids

    def stop_audit(self, audit_ids):

        audit_ids = [str(_[0]) for _ in audit_ids]
        audit_ids = ','.join(audit_ids)
        audit_ids = f'({audit_ids})'

        query = f'update audit set stop_time = now() where id in {audit_ids};'
        self.cursor.execute(query)

    def get_unprocessed_source(self):

        path_files = {path_file.as_posix() for path_file in self.path_source.iterdir()}

        query = f"select source from audit where process_name = '{self.process_name}' and stop_time is not null;"
        self.cursor.execute(query)
        path_processed_files = self.cursor.fetchall()
        path_processed_files = {path_processed_file[0] for path_processed_file in path_processed_files}

        path_unprocessed_files = path_files - path_processed_files

        return path_unprocessed_files

    def get_destination(self):
        path = self.path_destination / f'{uuid.uuid1()}.csv'
        return path.as_posix()

    def write_bad_data(self, bad_data):
        values = bad_data.apply(lambda row: f"({row['url_id']},'{row['error']}','{self.process_name}')", axis=1)
        values = ','.join(values)
        query = f'insert into errors (url_id, error, process_name) values {values};'
        self.cursor.execute(query)
