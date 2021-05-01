import numpy as np
import pandas as pd
import umap
from pyspark.sql.functions import array_contains

from aggregator.data_platform.utils import function
from aggregator.data_platform.utils.etls.load_parquet_etl import LoadParquetEtl


class PointsEtl(LoadParquetEtl):

    def __init__(self, spark, path_source, path_target):
        super().__init__(path_target)
        self.spark = spark
        self.path_source = path_source

    def extract(self):
        df_embeddings = function.read_delta(self.spark, self.path_source)
        return df_embeddings

    def transform(self, df_embeddings):

        df_embeddings = df_embeddings \
            .select('url_id', 'embedding_document') \
            .filter(~array_contains('embedding_document', np.nan)) \
            .toPandas()

        embeddings = df_embeddings['embedding_document'].to_list()
        embeddings = np.array(embeddings, dtype=np.float32)

        model_umap = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine')

        points = model_umap.fit_transform(embeddings)

        df_points = pd.DataFrame()
        df_points['url_id'] = df_embeddings['url_id']
        df_points['point'] = points.tolist()

        return df_points
