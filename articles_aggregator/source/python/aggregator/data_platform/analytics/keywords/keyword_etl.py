import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from aggregator.data_platform.utils.auditable_etl import AuditableEtl
from aggregator.data_platform.utils.function import read_parquet


# todo refactor
class KeywordEtl(AuditableEtl):

    def __init__(self, path_idf, n_words=5, **kwargs):
        super().__init__(**kwargs, destination_extension='parquet')

        self.n_words = n_words

        self.model_word2idf = pd.read_csv(path_idf)
        self.model_word2idf = dict(zip(self.model_word2idf['token'], self.model_word2idf['idf']))

    def extract(self, source):
        return read_parquet(paths=source)

    def transform(self, data):
        processed = data[['url_id']]
        processed['document_keywords'] = data['document'].map(self.get_keywords)
        return processed

    def load(self, data, destination):
        data.to_parquet(destination, index=False)

    def get_keywords(self, document: str):

        vectorizer_tf = TfidfVectorizer(norm='l1', use_idf=False)
        tf = vectorizer_tf.fit_transform([document])
        tf = tf.toarray()[0]

        tokens = vectorizer_tf.get_feature_names()

        idf = np.array([self.model_word2idf.get(token, 0.0) for token in tokens])

        tf_idf = tf * idf

        index_keywords = tf_idf.argsort()[-self.n_words:][::-1]
        keywords = np.array(tokens)[index_keywords]

        return keywords
