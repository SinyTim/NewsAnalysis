import gensim
import pandas as pd
from pathlib import Path
import multiprocessing
import logging

from aggregator.data_platform.utils import read_dir_parquet


def main():

    path_data = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\preprocessed')
    path_word2vec = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\word2vec\model.model')

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    cores = multiprocessing.cpu_count()

    data = read_dir_parquet(path_data)
    documents = pd.concat((data['document'], data['header']), ignore_index=True)
    documents = documents.str.split()
    documents = documents.tolist()

    params_word2vec = {
        'size': 300,
        'window': 5,
        'min_count': 20,
        'workers': cores,
        'sg': 1,
        'negative': 5,
        'sample': 1e-5,
        'iter': 150,
    }

    model = gensim.models.Word2Vec(sentences=documents, **params_word2vec)

    model.save(str(path_word2vec))


if __name__ == '__main__':
    main()
