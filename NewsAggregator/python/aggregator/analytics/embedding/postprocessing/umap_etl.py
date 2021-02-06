import pickle

import numpy as np

from aggregator.utils.auditable_etl import AuditableEtl
from aggregator.utils.function import read_parquet


class UmapEtl(AuditableEtl):

    def __init__(self, path_umap, **kwargs):
        super().__init__(**kwargs, destination_extension='parquet')

        with open(path_umap, 'rb') as file:
            self.model_umap = pickle.load(file)

    def extract(self, source):
        return read_parquet(paths=source)

    def transform(self, data):

        embeddings = data['document'].to_list()
        embeddings = np.array(embeddings, dtype=np.float32)

        embeddings = self.model_umap.transform(embeddings)

        processed = data[['url_id']]
        processed['document'] = embeddings.tolist()

        return processed

    def load(self, data, destination):
        data.to_parquet(destination, index=False)
