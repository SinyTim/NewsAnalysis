from pathlib import Path

from pyspark.sql import SparkSession

from aggregator.data_platform.utils.function import read_delta


def main():
    pass

    # spark = SparkSession.builder \
    #     .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
    #     .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
    #     .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
    #     .config('spark.driver.memory', '8g') \
    #     .getOrCreate()
    #
    # path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\curated\article.delta')
    #
    # df = read_delta(spark, path)


if __name__ == '__main__':
    main()
