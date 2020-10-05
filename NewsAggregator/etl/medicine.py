import pandas as pd
from pathlib import Path
import numpy as np


if __name__ == '__main__':

    path_landing = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_datalake\landing\medicine')
    path_out = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_datalake\documents_data\medicine.parquet')

    dfs = [pd.read_csv(path) for path in path_landing.iterdir()]
    df = pd.concat(dfs, ignore_index=True)

    df = df[['url', 'header', 'time', 'document']]

    df['source'] = 'medicine'
    df['tags'] = None

    assert df['url'].is_unique

    df.to_parquet(path_out, index=False)
