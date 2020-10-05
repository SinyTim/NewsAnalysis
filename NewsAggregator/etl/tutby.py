import pandas as pd
from pathlib import Path


if __name__ == '__main__':

    path_landing = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_datalake\landing\tutby')
    path_out = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_datalake\documents_data\tutby.parquet')

    dfs = [pd.read_csv(path, parse_dates=True, infer_datetime_format=True) for path in path_landing.iterdir()]
    df = pd.concat(dfs, ignore_index=True)

    df = df[['url', 'header', 'time', 'document', 'tags']]

    df['source'] = 'tutby'

    assert df['url'].is_unique

    df.to_parquet(path_out, index=False)
