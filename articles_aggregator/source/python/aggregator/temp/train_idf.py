from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def main():

    path_data = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\corpora\clean_tutby_126784.csv')
    # path_data = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\preprocessed')
    path_idf = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\idf.csv')

    # data = read_dir_parquet(path_data)
    # data = data['document']
    data = pd.read_csv(path_data)
    data = data['document'].fillna('')

    vectorizer_idf = TfidfVectorizer(norm='l1', use_idf=True, min_df=100, max_df=0.97)
    vectorizer_idf.fit(data)

    idf = vectorizer_idf.idf_
    vocabulary = vectorizer_idf.get_feature_names()

    df = pd.DataFrame(zip(vocabulary, idf), columns=['token', 'idf'])
    df.to_csv(path_idf, index=False)


if __name__ == '__main__':
    main()
