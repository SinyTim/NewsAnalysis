from pyspark.sql.functions import col
from pyspark.sql.functions import lit
from pyspark.sql.functions import to_timestamp

from aggregator.data_platform.utils.incremental_delta_etl import IncrementalDeltaEtl


class StructuredToCuratedEtl(IncrementalDeltaEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.columns_target = [
            ('url_id', 'string'),
            ('header', 'string'),
            ('document', 'string'),
            ('time', 'string'),
            ('tags', 'array<string>'),
        ]

    def transform(self, df):

        columns = [
            name if name in df.columns else lit(None).cast(column_type).alias(name)
            for name, column_type in self.columns_target
        ]

        df = df \
            .select(*columns) \
            .withColumn('time', to_timestamp('time', format='yyyy-MM-dd HH:mm'))

        # df_bad = df \
        #     .filter(col('document').isNull() | (col('document') == '')) \
        #     .select('url_id', lit('empty document').alias('error'))

        df = df.filter(col('document').isNotNull() & (col('document') != ''))

        return df
