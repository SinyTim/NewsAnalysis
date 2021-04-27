from pyspark.sql.functions import col
from pyspark.sql.functions import udf
from pyspark.storagelevel import StorageLevel

from aggregator.data_platform.utils.incremental_delta_etl import IncrementalDeltaEtl


class StructuredHtmlEtl(IncrementalDeltaEtl):

    def __init__(self, parse_return_type, **kwargs):
        super().__init__(**kwargs)
        self.parse_return_type = f'{parse_return_type}, error string'

    def transform(self, df_html):

        parser = self.get_parser()
        parse_html = udf(parser, returnType=self.parse_return_type)

        n_partitions_init = df_html.rdd.getNumPartitions()

        size_partition = 10
        n_htmls = df_html.count()
        n_partitions = n_htmls // size_partition
        n_partitions = max(n_partitions, 1)

        df_html = df_html \
            .repartition(n_partitions) \
            .persist(storageLevel=StorageLevel.DISK_ONLY)

        df = df_html \
            .withColumn('html', parse_html('html')) \
            .select('url_id', 'html.*') \
            .repartition(n_partitions_init)

        # df = df.cahce()

        df_parsed = df \
            .filter(col('error').isNull()) \
            .drop('error')

        # df_bad = df \
        #     .filter(col('error').isNotNull()) \
        #     .select('url_id', 'error')

        return df_parsed

    def get_parser(self):
        raise NotImplementedError
