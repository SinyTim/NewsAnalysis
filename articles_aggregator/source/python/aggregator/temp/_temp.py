from pathlib import Path

import pandas as pd

from aggregator.data_platform.utils.function import read_parquet


if __name__ == '__main__':

    pd.set_option('display.max_columns', 10)

    path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\topicwords')
    df = read_parquet(path)

    print(df)
