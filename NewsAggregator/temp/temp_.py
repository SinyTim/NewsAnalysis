import pandas as pd
from pathlib import Path


if __name__ == '__main__':

    path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\documents_data')

    dfs = [pd.read_parquet(p) for p in path.iterdir()]
    df = pd.concat(dfs, ignore_index=True)

    df = df.sort_values('time')

    pd.set_option('display.max_columns', 10)
    print(df.head(30))
