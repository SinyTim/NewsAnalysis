import hdbscan
import numpy as np

from aggregator.data_platform.utils import function


class ClusteringEtl:

    def __init__(self, spark, path_source, path_target, full_reload=True):

        self.spark = spark
        self.path_source = path_source
        self.path_target = path_target

        self.full_reload = full_reload

    def run(self):
        df = self.extract()
        df = self.transform(df)
        self.load(df)

    def extract(self):
        return function.read_delta(self.spark, self.path_source)

    def load(self, df):
        function.write_delta(df, self.path_target, mode='overwrite')

    def transform(self, df):

        data = df.toPandas()
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
        processed = self.spark.createDataFrame(processed)

        return processed
