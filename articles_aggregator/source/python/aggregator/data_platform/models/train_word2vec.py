import logging
import multiprocessing
from pathlib import Path

import gensim
from pyspark.sql import SparkSession

from aggregator.data_platform.utils import function


def main():

    path_source = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\analytics\preprocessed.delta')
    path_model = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\models\word2vec\model.model')

    spark = SparkSession.builder \
        .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .getOrCreate()

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    n_cores = multiprocessing.cpu_count()

    df = function.read_delta(spark, path_source)
    documents = df.select('document') \
        .union(df.select('header')) \
        .toPandas()['document']

    documents = documents.str.split()
    documents = documents.tolist()

    params_word2vec = {
        'size': 300,
        'window': 5,
        'min_count': 20,
        'workers': n_cores,
        'sg': 1,
        'negative': 5,
        'sample': 1e-5,
        'iter': 2,  # 150
    }

    model = gensim.models.Word2Vec(sentences=documents, **params_word2vec)

    model.save(str(path_model))


if __name__ == '__main__':
    main()
