from pathlib import Path
import pandas as pd
import uuid

from utils.auditable_etl import AuditableEtl


class StageToDwEtl(AuditableEtl):

    def __init__(self, process_name, path_source: Path, path_destination: Path):
        super().__init__()
        self.process_name = process_name
        self.path_source = path_source
        self.path_destination = path_destination
        self.columns = ['url_id', 'header', 'time', 'document', 'tags']

        self.path_destination.mkdir(exist_ok=True)

    def extract(self, source):
        data = [pd.read_csv(path_file, parse_dates=True, infer_datetime_format=True) for path_file in source]
        data = pd.concat(data, ignore_index=True)
        return data

    def transform(self, data):

        existing_columns = set(data.columns)
        load_columns = set(self.columns)
        not_existing_columns = list(load_columns - existing_columns)

        data = data[existing_columns & load_columns]

        for column_name in not_existing_columns:
            data = data.assign(**{column_name: None})

        bad_data = data[['url_id']][data['document'].isna()]
        bad_data['error'] = 'empty document'
        data = data.drop(bad_data.index)

        return data, bad_data

    def load(self, data, destination):
        data, bad_data = data

        data.to_parquet(destination, index=False)

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
        path = self.path_destination / f'{uuid.uuid1()}.parquet'
        return path.as_posix()

    def write_bad_data(self, bad_data):
        values = bad_data.apply(lambda row: f"({row['url_id']},'{row['error']}','{self.process_name}')", axis=1)
        values = ','.join(values)
        query = f'insert into errors (url_id, error, process_name) values {values};'
        self.cursor.execute(query)
