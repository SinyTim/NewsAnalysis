from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import floor


# todo move
def repartition_delta(spark, path, n_partitions):

    spark \
        .read \
        .format('delta') \
        .load(path) \
        .repartition(n_partitions) \
        .write \
        .option('dataChange', 'false') \
        .format('delta') \
        .mode('overwrite') \
        .save(path)

    query = f'vacuum delta.`{path}` retain 0 hours'
    spark.sql(query)


def repartition_by_column_delta(spark, path):

    name_column_partition = '_time_updated_period'
    period_seconds = 10 * 24 * 60 * 60

    column_timestamp = col('_time_updated').cast('bigint')
    column_period = floor(column_timestamp / period_seconds)

    spark \
        .read \
        .format('delta') \
        .load(path) \
        .withColumn(name_column_partition, column_period) \
        .write \
        .format('delta') \
        .partitionBy(name_column_partition) \
        .option('overwriteSchema', 'true') \
        .mode('overwrite') \
        .save(path)

    query = f'vacuum delta.`{path}` retain 0 hours'
    spark.sql(query)


def main():

    spark = SparkSession.builder \
        .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .config('spark.databricks.delta.retentionDurationCheck.enabled', 'false') \
        .config('spark.driver.memory', '8g') \
        .getOrCreate()

    path = r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\analytics\preprocessed.delta'
    n_partitions = 256

    # repartition_delta(spark, path, n_partitions)
    repartition_by_column_delta(spark, path)


if __name__ == '__main__':
    main()
