from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def main():

    path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\preprocessed')
    path_save = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\idf.csv')

    data = [pd.read_parquet(path_file) for path_file in path.iterdir()]
    data = pd.concat(data, ignore_index=True, sort=True)
    data = data['document']
    print(data.shape)

    vectorizer_idf = TfidfVectorizer(norm='l1', use_idf=True)
    vectorizer_idf.fit(data)

    idf = vectorizer_idf.idf_
    # idf = idf / idf.sum()
    vocabulary = vectorizer_idf.get_feature_names()

    df = pd.DataFrame(zip(vocabulary, idf), columns=['token', 'idf'])
    df.to_csv(path_save, index=False)


if __name__ == '__main__':
    main()
