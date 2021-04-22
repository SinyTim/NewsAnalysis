from pyspark.sql import SparkSession


if __name__ == '__main__':

    spark = SparkSession.builder \
        .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .config('spark.driver.memory', '8g') \
        .getOrCreate()

    path = r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\raw\html\tutby.delta'
    n_partitions = 128

    (spark.read
     .format('delta')
     .load(path)
     .repartition(n_partitions)
     .write
     .option('dataChange', 'false')
     .format('delta')
     .mode('overwrite')
     .save(path))
