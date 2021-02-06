from pathlib import Path

import pandas as pd

from aggregator.utils.function import read_parquet


if __name__ == '__main__':

    pd.set_option('display.max_columns', 10)

    path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\preprocessed')
    df = read_parquet(path)

    print(df[df['url_id'] == 614]['document'].iloc[0])
