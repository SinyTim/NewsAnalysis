from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import lit

from aggregator.data_platform.utils.function import read_delta
from aggregator.data_platform.utils.function import read_parquet


if __name__ == '__main__':

    # pd.set_option('display.max_columns', 10)
    #
    # path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\topicwords')
    # df = read_parquet(path)
    #
    # print(df)

    spark = SparkSession.builder \
        .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .getOrCreate()

    # path0 = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\curated\article.delta')
    # path1 = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\analytics\preprocessed.delta')
    #
    # df0 = read_delta(spark, path0)
    # df1 = read_delta(spark, path1)
    #
    # df = df0.join(df1, on='url_id')
    #
    # print(df.show(3, True))

    path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\analytics\topicwords.delta')
    df = read_delta(spark, path)  # .filter(col('url_id') == lit('7549ab70-a2c5-11eb-b579-e1b220426efd-41032'))
    print(df.count())
    print(df.show(5, False))
