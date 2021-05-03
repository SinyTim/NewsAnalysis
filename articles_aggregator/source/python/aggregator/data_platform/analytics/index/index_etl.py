from pathlib import Path

import faiss
import numpy as np
from pyspark.sql.functions import array_contains

from aggregator.data_platform.utils.etls.incremental_delta_etl import IncrementalDeltaEtl


# todo
class IndexEtl(IncrementalDeltaEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transform(self, df):

        df = df.select('url_id', 'embedding_document') \
            .filter(~array_contains('embedding_document', np.nan)) \
            .toPandas()

        embeddings = df['embedding_document'].tolist()
        embeddings = np.array(embeddings, dtype=np.float32)

        labels = df['url_id'].to_numpy()

        if Path(self.path_target).exists():
            index = faiss.read_index(self.path_target)
        else:
            dim = embeddings.shape[1]
            index = faiss.index_factory(dim, 'IDMap,L2norm,Flat')

        # labels must be int64
        # labels = np.arange(len(embeddings)).astype(np.int64)
        index.add_with_ids(embeddings, labels)

        return index

    def load(self, index):
        faiss.write_index(index, str(self.path_target))
