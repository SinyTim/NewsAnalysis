from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.etl import Etl


class ExportEtl(Etl):

    def __init__(self, spark, path_source, path_target):
        self.spark = spark
        self.path_source = path_source
        self.path_target = path_target

    def extract(self):
        return function.read_delta(self.spark, self.path_source)

    def transform(self, df):
        return df.coalesce(1)

    def load(self, df):
        function.write_json(df, self.path_target)
