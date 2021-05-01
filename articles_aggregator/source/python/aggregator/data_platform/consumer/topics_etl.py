from pyspark.sql.functions import count
from pyspark.sql.functions import desc

from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.load_parquet_etl import LoadParquetEtl


class TopicsEtl(LoadParquetEtl):

    def __init__(self, spark, path_source_clustering, path_source_topicwords, path_target):
        super().__init__(path_target)

        self.spark = spark

        self.path_source_clustering = path_source_clustering
        self.path_source_topicwords = path_source_topicwords

    def extract(self):
        df_clustering = function.read_delta(self.spark, self.path_source_clustering)
        df_topicwords = function.read_delta(self.spark, self.path_source_topicwords)
        return df_clustering, df_topicwords

    def transform(self, data):
        df_clustering, df_topicwords = data

        df_topics = df_clustering \
            .groupBy('topic_id') \
            .agg(count('url_id').alias('topic_size')) \
            .join(df_topicwords, on='topic_id') \
            .orderBy(desc('topic_size')) \
            .toPandas()

        return df_topics
