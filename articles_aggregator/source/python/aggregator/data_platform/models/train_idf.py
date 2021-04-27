from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession
from sklearn.feature_extraction.text import TfidfVectorizer

from aggregator.data_platform.utils.model_etl import ModelEtl


class IdfModelEtl(ModelEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transform(self, df):

        documents = df \
            .select('document') \
            .toPandas()['document']

        vectorizer_idf = TfidfVectorizer(norm='l1', use_idf=True, min_df=100, max_df=0.97)
        vectorizer_idf.fit(documents)

        idf = vectorizer_idf.idf_
        vocabulary = vectorizer_idf.get_feature_names()

        df = pd.DataFrame(zip(vocabulary, idf), columns=['token', 'idf'])

        return df

    def load(self, model):
        model.to_csv(self.path_model, index=False)


def main():

    spark = SparkSession.builder \
        .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .config('spark.driver.memory', '8g') \
        .getOrCreate()

    params = {
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\analytics\preprocessed.delta'),
        'path_model': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data\models\idf\idf.csv'),
        'spark': spark,
    }

    IdfModelEtl(**params).run()


if __name__ == '__main__':
    main()
