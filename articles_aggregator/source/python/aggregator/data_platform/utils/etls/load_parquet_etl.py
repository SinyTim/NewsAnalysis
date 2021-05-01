from abc import ABC

from aggregator.data_platform.utils.etls.etl import Etl


class LoadParquetEtl(Etl, ABC):

    def __init__(self, path_target):
        self.path_target = path_target

    def load(self, df):
        df.to_parquet(self.path_target, index=False)
