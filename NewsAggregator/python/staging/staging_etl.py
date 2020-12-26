import pandas as pd

from utils.auditable_etl import AuditableEtl


class StagingHtmlEtl(AuditableEtl):

    def __init__(self, columns, **kwargs):
        super().__init__(**kwargs, destination_extension='csv')
        self.columns = columns

    def parse_html(self, html):
        raise NotImplementedError

    def extract(self, source):
        data = [pd.read_csv(path_file) for path_file in source]
        data = pd.concat(data, ignore_index=True)
        return data

    def transform(self, data: pd.DataFrame):

        data['parsed'] = data['html'].map(self.parse_html)
        data = data.drop('html', axis=1)

        index_bad = data['parsed'].map(type) == str
        bad_data = data[index_bad]
        bad_data = bad_data.rename(columns={'parsed': 'error'})

        data = data[~index_bad]

        data_parsed = data['parsed'].apply(pd.Series)
        data_parsed.columns = self.columns
        data = pd.concat((data, data_parsed), axis=1)
        data = data.drop('parsed', axis=1)

        return data, bad_data

    def load(self, data, destination):
        data, bad_data = data

        data.to_csv(destination, index=False)

        if len(bad_data) != 0:
            self.write_bad_data(bad_data)
