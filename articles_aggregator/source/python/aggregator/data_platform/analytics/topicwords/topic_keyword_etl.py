import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from aggregator.data_platform.utils.auditable_etl import AuditableEtl
from aggregator.data_platform.utils.function import read_parquet


class TopicKeywordEtl(AuditableEtl):

    def __init__(self, path_documents, path_topic_ids, path_idf, n_words=5, **kwargs):
        super().__init__(**kwargs, destination_extension='parquet')

        self.path_documents = path_documents
        self.path_topic_ids = path_topic_ids

        self.n_words = n_words

        self.model_word2idf = pd.read_csv(path_idf)
        self.model_word2idf = dict(zip(self.model_word2idf['token'], self.model_word2idf['idf']))

    def run(self):
        destination = self.get_destination()
        data = self.extract(None)
        data = self.transform(data)
        self.load(data, destination)

    def extract(self, source):
        df_documents = read_parquet(path_dir=self.path_documents)
        df_topic_id = read_parquet(path_dir=self.path_topic_ids)
        return df_documents, df_topic_id

    def transform(self, data):
        df_documents, df_topic_id = data

        df = df_documents.merge(df_topic_id, how='inner', on='url_id')
        df = df[df['topic_id'] != -1]

        topic_documents = df.groupby('topic_id').agg({'document': ' '.join})

        vectorizer_tf = TfidfVectorizer(norm='l1', use_idf=False)
        tf = vectorizer_tf.fit_transform(topic_documents['document'])

        tokens = vectorizer_tf.get_feature_names()
        idf = [self.model_word2idf[token] if token in self.model_word2idf else 0.0 for token in tokens]
        idf = np.array(idf)

        tf_idf = np.multiply(tf.todense(), idf ** 2)

        index = tf_idf.argsort(axis=1)[:, -self.n_words:][:, ::-1]
        topic_words = np.array(tokens)[index]

        df = pd.DataFrame()
        df['topic_id'] = topic_documents.index
        df['topic_words'] = topic_words.tolist()

        return df

    def load(self, data, destination):

        for path in self.path_destination.iterdir():
            path.unlink()

        data.to_parquet(destination, index=False)
