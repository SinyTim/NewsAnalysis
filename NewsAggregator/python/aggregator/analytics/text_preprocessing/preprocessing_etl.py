import re
import string

import nltk
import pandas as pd
import pymystem3

from aggregator.utils.auditable_etl import AuditableEtl


class PreprocessingEtl(AuditableEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, destination_extension='parquet')

        nltk.download('stopwords')
        self.russian_stop_words = nltk.corpus.stopwords.words('russian')
        self.russian_stop_words = set(self.russian_stop_words)

        self.mystem = pymystem3.Mystem()

    def extract(self, source):
        data = [pd.read_parquet(path_file) for path_file in source]
        data = pd.concat(data, ignore_index=True, sort=True)
        return data

    def transform(self, data):
        processed = data[['url_id']]
        processed['header'] = self.preprocess(data['header'])
        processed['document'] = self.preprocess(data['document'])
        return processed

    def load(self, data, destination):
        data.to_parquet(destination, index=False)

    def preprocess(self, corpus, batch_size=1000):

        separator = 'qsefthukoaxdvgnjthukoaxdvefcngwojd'
        corpus_processed = []

        for i in range(len(corpus) // batch_size + 1):
            batch = corpus[i * batch_size:(i + 1) * batch_size]
            batch_joint = f' {separator} '.join(batch)
            batch_clean = self.preprocess_document(batch_joint)
            batch_clean = batch_clean.split(separator)
            corpus_processed += batch_clean

        corpus_processed = [_.strip() for _ in corpus_processed]

        return corpus_processed

    def preprocess_document(self, document):
        document = document.lower()
        document = re.sub(u'\xa0|\n', ' ', document)
        document = re.sub('[^а-яa-z ]', '', document)
        # removing extra spaces...
        tokens = self.mystem.lemmatize(document)
        tokens = [token for token in tokens if
                  ((token not in self.russian_stop_words) and (token.strip() not in string.punctuation) and (
                              len(token) > 2))]
        document = ' '.join(tokens)
        return document
