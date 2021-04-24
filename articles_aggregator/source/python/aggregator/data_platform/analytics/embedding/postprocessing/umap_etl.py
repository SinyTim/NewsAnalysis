import pickle

import numpy as np
from pyspark.sql.functions import array_contains

from aggregator.data_platform.utils.incremental_delta_etl import IncrementalDeltaEtl


class UmapEtl(IncrementalDeltaEtl):

    def __init__(self, path_umap, **kwargs):
        super().__init__(**kwargs)

        with open(path_umap, 'rb') as file:
            self.model_umap = pickle.load(file)

    def transform(self, df):

        # todo separate embeddings tables for header and document because they not always exists both.
        #  filter them for np.nan
        #  remove filter here.
        df = df.select('url_id', 'embedding_document') \
            .filter(~array_contains('embedding_document', np.nan)) \
            .toPandas()

        embeddings = df['embedding_document'].to_list()
        embeddings = np.array(embeddings, dtype=np.float32)

        embeddings = self.model_umap.transform(embeddings)

        processed = df[['url_id']]
        processed['embedding_document'] = embeddings.tolist()
        processed = self.spark.createDataFrame(processed)

        return processed
