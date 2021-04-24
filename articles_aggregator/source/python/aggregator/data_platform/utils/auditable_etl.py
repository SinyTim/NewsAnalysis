import uuid
from pathlib import Path

import pandas as pd
import psycopg2


# todo remove
class AuditableEtl:

    def __init__(self, process_name: str,
                 path_destination: Path,
                 path_source: Path = None,
                 destination_extension: str = None):

        self.path_source = path_source
        self.path_destination = path_destination
        self.process_name = process_name
        self.destination_extension = destination_extension

        self.path_destination.mkdir(exist_ok=True)

        auditdb_url = '34.123.127.77'
        auditdb_name = 'dbaudit'
        user_name = 'postgres'
        user_password = 'P@ssw0rd'

        self.connection = psycopg2.connect(
            host=auditdb_url, database=auditdb_name,
            user=user_name, password=user_password
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def run(self):

        source = self.get_unprocessed_source()

        if not source:
            return

        destination = self.get_destination()

        audit_ids = self.start_audit(source, destination)

        data = self.extract(source)
        data = self.transform(data)
        self.load(data, destination)

        self.stop_audit(audit_ids)

    def extract(self, source):
        raise NotImplementedError

    def transform(self, data):
        raise NotImplementedError

    def load(self, data, destination):
        raise NotImplementedError

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
        assert self.path_source is not None

        path_files = {path_file.as_posix() for path_file in self.path_source.iterdir()}

        query = f"select source from audit where process_name = '{self.process_name}' and stop_time is not null;"
        self.cursor.execute(query)
        path_processed_files = self.cursor.fetchall()
        path_processed_files = {path_processed_file[0] for path_processed_file in path_processed_files}

        path_unprocessed_files = path_files - path_processed_files

        return path_unprocessed_files

    def get_destination(self):
        destination_extension = f'.{self.destination_extension}' if self.destination_extension else ''
        path = self.path_destination / f'{uuid.uuid1()}{destination_extension}'
        return path.as_posix()

    def write_bad_data(self, bad_data: pd.DataFrame):
        values = bad_data.apply(lambda row: f"({row['url_id']},'{row['error']}','{self.process_name}')", axis=1)
        values = ','.join(values)
        query = f'insert into errors (url_id, error, process_name) values {values};'
        self.cursor.execute(query)
