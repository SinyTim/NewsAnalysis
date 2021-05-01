import gensim
import numpy as np
import pandas as pd
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType
from pyspark.sql.types import FloatType

from aggregator.data_platform.utils.etls.incremental_delta_etl import IncrementalDeltaEtl


class Word2vecEtl(IncrementalDeltaEtl):

    def __init__(self, path_word2vec, path_idf, **kwargs):
        super().__init__(**kwargs)

        path_word2vec = str(path_word2vec)
        self.model_word2vec = gensim.models.Word2Vec.load(path_word2vec)
        self.vocab_word2vec = set(self.model_word2vec.wv.vocab.keys())

        self.model_word2idf = pd.read_csv(path_idf)
        self.model_word2idf = dict(zip(self.model_word2idf['token'], self.model_word2idf['idf']))
        self.vocab_word2idf = set(self.model_word2idf.keys())

    def transform(self, df):

        get_embedding = self.get_udf()

        df = df.select(
            'url_id',
            get_embedding('header').alias('embedding_header'),
            get_embedding('document').alias('embedding_document'),
        )

        return df

    def get_udf(self):

        bc_vocab_word2vec = self.spark.sparkContext.broadcast(self.vocab_word2vec)
        bc_vocab_word2idf = self.spark.sparkContext.broadcast(self.vocab_word2idf)
        bc_model_word2vec = self.spark.sparkContext.broadcast(self.model_word2vec)
        bc_model_word2idf = self.spark.sparkContext.broadcast(self.model_word2idf)

        @udf(returnType=ArrayType(FloatType()))
        def get_embedding(document: str):

            tokens = document.split()
            tokens = [token for token in tokens if token in bc_vocab_word2vec.value]
            tokens = [token for token in tokens if token in bc_vocab_word2idf.value]

            if tokens:
                idfs = [bc_model_word2idf.value[token] for token in tokens]
                embeddings = bc_model_word2vec.value.wv[tokens]
                embedding = np.dot(embeddings.T, idfs)
            else:
                embedding = np.full(bc_model_word2vec.value.vector_size, np.nan)

            return embedding.tolist()

        return get_embedding
