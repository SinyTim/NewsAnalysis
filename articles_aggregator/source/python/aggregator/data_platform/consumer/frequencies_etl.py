import pandas as pd
from pyspark.sql.functions import col

from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.load_parquet_etl import LoadParquetEtl


class FrequenciesEtl(LoadParquetEtl):

    def __init__(self, spark, path_source_article, path_source_clustering, path_target):
        super().__init__(path_target)

        self.spark = spark

        self.path_source_article = path_source_article
        self.path_source_clustering = path_source_clustering

        self.resample_period = 'W'
        self.min_n_articles_per_period = 100

    def extract(self):
        df_article = function.read_delta(self.spark, self.path_source_article)
        df_clustering = function.read_delta(self.spark, self.path_source_clustering)
        return df_article, df_clustering

    def transform(self, data):
        df_article, df_clustering = data

        df_article_topic = df_article \
            .join(df_clustering, on='url_id') \
            .select('time', 'topic_id', 'url_id') \
            .filter(col('topic_id') != -1) \
            .orderBy('time') \
            .toPandas()

        df_article_topic = df_article_topic.set_index('time')
        ts_entire = df_article_topic.resample(self.resample_period)['url_id'].count()
        ts_topics = df_article_topic.groupby('topic_id').resample(self.resample_period)['url_id'].count()

        topic_ids = df_article_topic['topic_id'].unique()

        df_frequencies = pd.DataFrame(columns=['topic_id', 'time', 'frequency'])

        for topic_id in topic_ids:
            ts_topic = ts_topics[topic_id]
            ts_entire_indexed = ts_entire[ts_topic.index]
            ts = ts_topic / ts_entire_indexed
            ts = ts[ts_entire > self.min_n_articles_per_period]
            df = ts.reset_index().assign(**{'topic_id': topic_id}).rename(columns={'url_id': 'frequency'})
            df_frequencies = df_frequencies.append(df, ignore_index=True)

        return df_frequencies
