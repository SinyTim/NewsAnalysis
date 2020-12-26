import pandas as pd
from pathlib import Path


if __name__ == '__main__':

    pd.set_option('display.max_columns', 10)

    # path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\documents_data')
    # dfs = [pd.read_parquet(p) for p in path.iterdir()]
    # df = pd.concat(dfs, ignore_index=True, sort=True)
    # print(df[df['url_id'] == 444].head())
    #
    # path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\preprocessed\db07096a-4787-11eb-9a71-00059a3c7a00.parquet')
    # df = pd.read_parquet(path)
    # print(df[df['url_id'] == 444].head())

    path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\embeddings\7fcd75d7-47c0-11eb-b282-b58bfdff88ec.parquet')
    df = pd.read_parquet(path)
    print(df.head(3))
    print(type(df['document'].iloc[3]))
