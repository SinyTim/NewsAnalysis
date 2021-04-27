import numpy as np
import pandas as pd
from pyspark.sql.functions import col
from pyspark.sql.functions import collect_list
from pyspark.sql.functions import concat_ws
from sklearn.feature_extraction.text import TfidfVectorizer

from aggregator.data_platform.utils import function


class TopicKeywordEtl:

    def __init__(self, spark, path_source_topic_ids, path_source_documents, path_target, path_idf, n_words=5):

        self.spark = spark
        self.path_source_topic_ids = path_source_topic_ids
        self.path_source_documents = path_source_documents
        self.path_target = path_target

        self.n_words = n_words

        self.model_word2idf = pd.read_csv(path_idf)
        self.model_word2idf = dict(zip(self.model_word2idf['token'], self.model_word2idf['idf']))

    def run(self):
        data = self.extract()
        data = self.transform(data)
        self.load(data)

    def extract(self):
        df_topic_id = function.read_delta(self.spark, self.path_source_topic_ids)
        df_documents = function.read_delta(self.spark, self.path_source_documents)
        return df_documents, df_topic_id

    def load(self, df):
        function.write_delta(df, self.path_target, mode='overwrite')

    def transform(self, data):
        df_documents, df_topic_id = data

        topic_documents = df_documents \
            .join(df_topic_id, on='url_id', how='inner') \
            .filter(col('topic_id') != -1) \
            .groupBy('topic_id') \
            .agg(concat_ws(' ', collect_list('document')).alias('document')) \
            .toPandas()

        vectorizer_tf = TfidfVectorizer(norm='l1', use_idf=False)
        tf = vectorizer_tf.fit_transform(topic_documents['document'])

        tokens = vectorizer_tf.get_feature_names()
        idf = [self.model_word2idf.get(token, 0.0) for token in tokens]
        idf = np.array(idf)

        tf_idf = np.multiply(tf.todense(), idf ** 2)

        index = tf_idf.argsort(axis=1)[:, -self.n_words:][:, ::-1]
        topic_words = np.array(tokens)[index]

        df = pd.DataFrame()
        df['topic_id'] = topic_documents['topic_id']
        df['topic_words'] = topic_words.tolist()

        df = self.spark.createDataFrame(df)

        return df
