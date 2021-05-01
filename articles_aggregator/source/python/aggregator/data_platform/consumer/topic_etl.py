from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import count
from pyspark.sql.functions import desc

from aggregator.data_platform.utils.function import read_delta


def main():

    spark = SparkSession.builder \
        .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .config('spark.driver.memory', '8g') \
        .getOrCreate()

    path_lake = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data')

    path_url = path_lake / Path('raw/url')
    path_article = path_lake / Path('curated/article.delta')
    path_clustring = path_lake / Path('analytics/clustring.delta')
    path_topicwords = path_lake / Path('analytics/topicwords.delta')

    path_topics = path_lake / Path('consumer/topics.parquet')
    path_article_topic = path_lake / Path('consumer/article_topic.parquet')
    path_frequencies = path_lake / Path('consumer/frequencies.parquet')

    path_topics.parent.mkdir(exist_ok=True)

    df_article = read_delta(spark, path_article)
    df_clustring = read_delta(spark, path_clustring)
    df_topicwords = read_delta(spark, path_topicwords)

    df_topics = df_clustring \
        .groupBy('topic_id') \
        .agg(count('url_id').alias('topic_size')) \
        .join(df_topicwords, on='topic_id') \
        .orderBy(desc('topic_size')) \
        .toPandas()
    df_topics.to_parquet(path_topics, index=False)

    df_article_topic = df_article \
        .join(df_clustring, on='url_id') \
        .select('time', 'header', 'tags', 'topic_id') \
        .filter(col('topic_id') != -1) \
        .orderBy('time') \
        .toPandas() \
        .set_index('time')
    df_article_topic.to_parquet(path_article_topic, index=True)

    period = 'W'
    min_articles_per_period = 100

    ts_entire = df_article_topic.resample(period)['header'].count()
    ts_topics = df_article_topic.groupby('topic_id').resample(period)['header'].count()

    topic_ids = df_article_topic['topic_id'].unique()

    df_frequencies = pd.DataFrame(columns=['topic_id', 'time', 'frequency'])

    for topic_id in topic_ids:
        ts_topic = ts_topics[topic_id]
        ts_entire_indexed = ts_entire[ts_topic.index]
        ts = ts_topic / ts_entire_indexed
        ts = ts[ts_entire > min_articles_per_period]
        df = ts.reset_index().assign(**{'topic_id': topic_id}).rename(columns={'header': 'frequency'})
        df_frequencies = df_frequencies.append(df, ignore_index=True)

    df_frequencies.to_parquet(path_frequencies, index=False)


if __name__ == '__main__':
    main()
