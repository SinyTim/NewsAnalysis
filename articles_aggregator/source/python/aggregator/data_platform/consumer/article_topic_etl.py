from pyspark.sql.functions import col

from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.load_parquet_etl import LoadParquetEtl


class ArticleTopicEtl(LoadParquetEtl):

    def __init__(self, spark, path_source_article, path_source_clustering, path_target):
        super().__init__(path_target)

        self.spark = spark

        self.path_source_article = path_source_article
        self.path_source_clustering = path_source_clustering

    def extract(self):
        df_article = function.read_delta(self.spark, self.path_source_article)
        df_clustering = function.read_delta(self.spark, self.path_source_clustering)
        return df_article, df_clustering

    def transform(self, data):
        df_article, df_clustering = data

        df_article_topic = df_article \
            .join(df_clustering, on='url_id') \
            .select('time', 'header', 'tags', 'topic_id', 'url_id') \
            .filter(col('topic_id') != -1) \
            .orderBy('time') \
            .toPandas()

        return df_article_topic
