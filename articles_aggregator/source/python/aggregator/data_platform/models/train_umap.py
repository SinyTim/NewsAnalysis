import pickle
from pathlib import Path

import numpy as np
import umap
from pyspark.sql import SparkSession
from pyspark.sql.functions import array_contains

from aggregator.data_platform.utils.model_etl import ModelEtl


class UmapModelEtl(ModelEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transform(self, df):

        embeddings = df \
            .select('embedding_document') \
            .filter(~array_contains('embedding_document', np.nan)) \
            .toPandas()['embedding_document'] \
            .to_list()

        embeddings = np.array(embeddings, dtype=np.float32)

        model = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine')

        model.fit(embeddings)

    def load(self, model):
        with open(self.path_model, 'wb') as file:
            pickle.dump(model, file)


def main():

    spark = SparkSession.builder \
        .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .getOrCreate()

    params = {
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\analytics\embedding.delta'),
        'path_model': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\models\umap\umap.pickle'),
        'spark': spark,
    }

    UmapModelEtl(**params).run()


if __name__ == '__main__':
    main()
