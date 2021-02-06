from pathlib import Path

import faiss
import numpy as np

from aggregator.utils.auditable_etl import AuditableEtl
from aggregator.utils.function import read_parquet


class IndexEtl(AuditableEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name_index = 'index.faiss'
        self.name_column_document = 'document'
        self.name_column_label = 'url_id'

    def extract(self, path_embeddings):

        data = read_parquet(paths=path_embeddings)

        path_index = self.get_destination()
        index = faiss.read_index(path_index) if Path(path_index).exists() else None

        return data, index

    def transform(self, data):
        data, index = data

        embeddings = data[self.name_column_document].tolist()
        embeddings = np.array(embeddings, dtype=np.float32)
        labels = data[self.name_column_label].to_numpy()

        if not index:
            dim = embeddings.shape[1]
            index = faiss.index_factory(dim, 'IDMap,L2norm,Flat')

        index.add_with_ids(embeddings, labels)

        return index

    def load(self, index, path_index):
        faiss.write_index(index, str(path_index))

    def get_destination(self):
        path = self.path_destination / self.name_index
        return path.as_posix()
