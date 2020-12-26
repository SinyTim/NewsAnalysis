import pandas as pd

from utils.auditable_etl import AuditableEtl


class StageToDwEtl(AuditableEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, destination_extension='parquet')
        self.columns = ['url_id', 'header', 'time', 'document', 'tags']

    def extract(self, source):
        data = [pd.read_csv(path_file) for path_file in source]
        data = pd.concat(data, ignore_index=True)
        return data

    def transform(self, data):

        existing_columns = set(data.columns)
        load_columns = set(self.columns)
        load_existing_columns = list(load_columns & existing_columns)
        not_existing_columns = list(load_columns - existing_columns)

        load_existing_columns.sort()
        not_existing_columns.sort()

        data = data[load_existing_columns]

        for column_name in not_existing_columns:
            data = data.assign(**{column_name: None})

        data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M')

        index_bad = data['document'].isna()

        bad_data = data[['url_id']][index_bad]
        bad_data['error'] = 'empty document'

        data = data[~index_bad]

        return data, bad_data

    def load(self, data, destination):
        data, bad_data = data

        data.to_parquet(destination, index=False)

        if len(bad_data) != 0:
            self.write_bad_data(bad_data)
