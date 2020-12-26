import gensim
import numpy as np
import pandas as pd

from utils.auditable_etl import AuditableEtl


class Word2vecEtl(AuditableEtl):

    def __init__(self, path_word2vec, path_idf, **kwargs):
        super().__init__(**kwargs, destination_extension='parquet')

        path_word2vec = str(path_word2vec)
        self.model_word2vec = gensim.models.Word2Vec.load(path_word2vec)
        self.word2vec_vocab = self.model_word2vec.wv.vocab.keys()

        self.model_word2idf = pd.read_csv(path_idf)
        self.model_word2idf = dict(zip(self.model_word2idf['token'], self.model_word2idf['idf']))
        self.word2idf_vocab = self.model_word2idf.keys()

    def extract(self, source):
        data = [pd.read_parquet(path_file) for path_file in source]
        data = pd.concat(data, ignore_index=True, sort=True)
        return data

    def transform(self, data):
        processed = data[['url_id']]
        processed['header'] = data['header'].map(self.infer_document)
        processed['document'] = data['document'].map(self.infer_document)
        return processed

    def load(self, data, destination):
        data.to_parquet(destination, index=False)

    def infer_document(self, document: str):

        tokens = document.split()
        tokens = [token for token in tokens if token in self.word2vec_vocab]
        tokens = [token for token in tokens if token in self.word2idf_vocab]

        if tokens:
            idfs = [self.model_word2idf[token] for token in tokens]
            embeddings = self.model_word2vec.wv[tokens]
            embedding = np.dot(embeddings.T, idfs)
        else:
            embedding = np.full(self.model_word2vec.vector_size, np.nan)

        return embedding
