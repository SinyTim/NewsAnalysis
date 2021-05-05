import numpy as np
from pyspark.sql.functions import array_contains
from pyspark.sql.functions import col

from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.load_parquet_etl import LoadParquetEtl


class ArticleEtl(LoadParquetEtl):

    def __init__(self, spark, path_source_article, path_source_clustering, path_source_embeddings,
                 path_target):
        super().__init__(path_target)

        self.spark = spark

        self.path_source_article = path_source_article
        self.path_source_clustering = path_source_clustering
        self.path_source_embeddings = path_source_embeddings

    def extract(self):
        df_article = function.read_delta(self.spark, self.path_source_article)
        df_clustering = function.read_delta(self.spark, self.path_source_clustering)
        df_embeddings = function.read_delta(self.spark, self.path_source_embeddings)
        return df_article, df_clustering, df_embeddings

    def transform(self, data):
        df_article, df_clustering, df_embeddings = data

        df_article_topic = df_article \
            .join(df_clustering, on='url_id') \
            .join(df_embeddings, on='url_id') \
            .select('url_id', 'time', 'header', 'tags', 'topic_id', 'embedding_document') \
            .filter(col('topic_id') != -1) \
            .filter(~array_contains('embedding_document', np.nan)) \
            .orderBy('time') \
            .toPandas()

        n_articles = 50000
        df_article_topic = df_article_topic.iloc[-n_articles:]

        return df_article_topic
