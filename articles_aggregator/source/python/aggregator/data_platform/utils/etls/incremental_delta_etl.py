from abc import ABC
from datetime import datetime

from pyspark.sql.functions import col
from pyspark.sql.functions import current_timestamp
from pyspark.sql.functions import floor
from pyspark.sql.functions import lit

from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.incremental_etl import IncrementalEtl


class IncrementalDeltaEtl(IncrementalEtl, ABC):

    def __init__(self, spark, path_source, path_target, **kwargs):
        super().__init__(**kwargs, default_start_state='1971-01-01 00:00:00.000000')

        self.spark = spark
        self.path_source = path_source
        self.path_target = path_target

        self.period_seconds = 10 * 24 * 60 * 60

    def extract(self, start_state):

        start_state_parsed = datetime.strptime(start_state, '%Y-%m-%d %H:%M:%S.%f')
        start_state_parsed = datetime.timestamp(start_state_parsed)
        start_state_period = int(start_state_parsed) // self.period_seconds

        df = function.read_delta(self.spark, self.path_source) \
            .filter(col('_time_updated_period') >= lit(start_state_period)) \
            .filter(col('_time_updated') > lit(start_state))

        stop_state = df \
            .agg({'_time_updated': 'max'}) \
            .collect()[0][0]

        stop_state = stop_state or start_state

        df = df.drop('_time_updated_period', '_time_updated')

        return df, stop_state

    def load(self, df):

        # if df.rdd.isEmpty():
        #     return

        column_timestamp = col('_time_updated').cast('bigint')
        column_period = floor(column_timestamp / self.period_seconds)

        df = df \
            .withColumn('_time_updated', current_timestamp()) \
            .withColumn('_time_updated_period', column_period)

        function.write_delta(df, self.path_target, name_column_partition='_time_updated_period')
