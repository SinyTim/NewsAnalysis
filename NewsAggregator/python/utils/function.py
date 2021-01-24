import pandas as pd
from pathlib import Path


def read_dir_parquet(path: Path):
    data = [pd.read_parquet(path_file) for path_file in path.iterdir()]
    data = pd.concat(data, ignore_index=True, sort=True)
    return data
