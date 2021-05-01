from abc import ABC

from pyspark.sql.functions import col
from pyspark.sql.functions import current_timestamp
from pyspark.sql.functions import lit

from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.incremental_etl import IncrementalEtl


class IncrementalDeltaEtl(IncrementalEtl, ABC):

    def __init__(self, spark, path_source, path_target, **kwargs):
        super().__init__(**kwargs, default_start_state='1677-09-21 00:12:43.145225')

        self.spark = spark
        self.path_source = path_source
        self.path_target = path_target

    def extract(self, start_state):

        df = function.read_delta(self.spark, self.path_source) \
            .filter(col('_time_updated') > lit(start_state))

        stop_state = df \
            .agg({'_time_updated': 'max'}) \
            .collect()[0][0]

        stop_state = stop_state or start_state

        df = df.drop('_time_updated')

        return df, stop_state

    def load(self, df):

        # if df.rdd.isEmpty():
        #     return

        df = df.withColumn('_time_updated', current_timestamp())
        function.write_delta(df, self.path_target)
