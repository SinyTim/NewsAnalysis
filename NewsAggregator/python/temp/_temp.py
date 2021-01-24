from pathlib import Path

import numpy as np
import pandas as pd

from utils.function import read_dir_parquet


if __name__ == '__main__':

    pd.set_option('display.max_columns', 10)

    path = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\preprocessed')
    df = read_dir_parquet(path)

    print(df[df['url_id'] == 614]['document'].iloc[0])
