import re
import string

import nltk
import pandas as pd
import pymystem3
from pyspark.sql.functions import pandas_udf

from aggregator.data_platform.utils.etls.incremental_delta_etl import IncrementalDeltaEtl


class PreprocessingEtl(IncrementalDeltaEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transform(self, df):

        preprocess = self.get_udf()

        df = df.select(
            'url_id',
            preprocess('header').alias('header'),
            preprocess('document').alias('document'),
        )

        return df

    def get_udf(self):

        nltk.download('stopwords')
        russian_stop_words = nltk.corpus.stopwords.words('russian')
        russian_stop_words = set(russian_stop_words)
        bc_russian_stop_words = self.spark.sparkContext.broadcast(russian_stop_words)

        @pandas_udf(returnType='string')
        def preprocess(documents: pd.Series) -> pd.Series:

            separator = 'qsefthukoaxdvgnjthukoaxdvefcngwojd'

            document = f' {separator} '.join(documents)
            document = preprocess_document(document, bc_russian_stop_words.value)
            documents = document.split(separator)

            documents = [_.strip() for _ in documents]

            return pd.Series(documents)

        return preprocess


def preprocess_document(document, russian_stop_words):

    document = document.lower()
    document = re.sub(u'\xa0|\n', ' ', document)
    document = re.sub('[^а-яa-z ]', '', document)

    mystem = pymystem3.Mystem()
    tokens = mystem.lemmatize(document)

    tokens = [
        token
        for token in tokens
        if ((token not in russian_stop_words)
            and (token.strip() not in string.punctuation)
            and (len(token) > 2))
    ]

    document = ' '.join(tokens)

    return document
