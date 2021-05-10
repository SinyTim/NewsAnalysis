import pandas as pd
from pyspark.sql.functions import col
from pyspark.sql.functions import current_timestamp
from pyspark.sql.functions import floor

from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.incremental_etl import IncrementalEtl


class UrlGenerator(IncrementalEtl):

    def __init__(self, spark, url_template: str, path_target, path_bad_data, **kwargs):
        super().__init__(**kwargs)

        self.spark = spark

        self.url_template = url_template

        self.path_target = path_target
        # self.path_bad_data = path_bad_data

    def extract(self, start_state):
        df_urls, df_urls_bad, stop_state = self.generate(start_state)
        return (df_urls, df_urls_bad), stop_state

    def transform(self, data):
        df_urls, df_urls_bad = data

        df_urls = function.add_id_column(df_urls)

        return df_urls, df_urls_bad

    def load(self, data):
        df_urls, df_urls_bad = data

        if not df_urls.empty:
            df_urls = self.spark.createDataFrame(df_urls)
            self.load_good(df_urls)

        # if not df_urls_bad.empty:
        #     self.load_bad(df_urls_bad)

    def load_good(self, df_urls: pd.DataFrame):
        # todo merge by url

        period_seconds = 10 * 24 * 60 * 60
        column_timestamp = col('_time_updated').cast('bigint')
        column_period = floor(column_timestamp / period_seconds)

        df_urls = df_urls \
            .withColumn('_time_updated', current_timestamp()) \
            .withColumn('_time_updated_period', column_period)

        function.write_delta(df_urls, self.path_target, name_column_partition='_time_updated_period')

    # def load_bad(self, df_urls_bad: pd.DataFrame):
    #     df_urls = self.spark.createDataFrame(df_urls_bad)
    #     function.write_delta(df_urls, self.path_bad_data)

    def generate(self, start_state):
        raise NotImplementedError

    def increment_state(self, state):
        raise NotImplementedError

    def get_url_with_state(self, state):
        state = self.state_to_str(state)
        url = self.url_template.format(state)
        return url
