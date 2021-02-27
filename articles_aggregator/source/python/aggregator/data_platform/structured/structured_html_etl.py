from pyspark.sql.functions import col
from pyspark.sql.functions import udf

from aggregator.data_platform.utils.incremental_delta_etl import IncrementalDeltaEtl


class StructuredHtmlEtl(IncrementalDeltaEtl):

    def __init__(self, parse_return_type, **kwargs):
        super().__init__(**kwargs)
        self.parse_return_type = f'{parse_return_type}, error string'

    def transform(self, df_html):
        df_html = df_html.repartition(100)  # todo check

        parser = self.get_parser()
        parse_html = udf(parser, returnType=self.parse_return_type)

        df = df_html \
            .withColumn('html', parse_html('html')) \
            .select('url_id', 'html.*')

        # df = df.cahce()

        df_parsed = df \
            .filter(col('error').isNull()) \
            .drop('error')

        df_bad = df \
            .filter(col('error').isNotNull()) \
            .select('url_id', 'error')

        return df_parsed

    def get_parser(self):
        raise NotImplementedError
