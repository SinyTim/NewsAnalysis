import hdbscan
import numpy as np

from aggregator.utils.auditable_etl import AuditableEtl
from aggregator.utils.function import read_parquet


class ClusteringEtl(AuditableEtl):

    def __init__(self, full_reload=True,  **kwargs):
        super().__init__(**kwargs, destination_extension='parquet')

        self.full_reload = full_reload

    def extract(self, source):
        return read_parquet(paths=source)

    def transform(self, data):

        embeddings = data['embedding_document'].to_list()
        embeddings = np.array(embeddings, dtype=np.float32)

        cluster = hdbscan.HDBSCAN(
            min_cluster_size=15,
            metric='euclidean',
            cluster_selection_method='eom'
        )

        cluster.fit(embeddings)

        processed = data[['url_id']]
        processed['topic_id'] = cluster.labels_

        return processed

    def load(self, data, destination):

        if self.full_reload:
            for path in self.path_destination.iterdir():
                path.unlink()

        data.to_parquet(destination, index=False)

    def get_unprocessed_source(self):
        if self.full_reload:
            path_files = {path_file.as_posix() for path_file in self.path_source.iterdir()}
            return path_files
        else:
            raise NotImplementedError
