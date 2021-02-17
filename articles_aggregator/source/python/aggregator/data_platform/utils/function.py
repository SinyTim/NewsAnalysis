from pathlib import Path

import pandas as pd


def read_parquet(path_dir: Path = None, paths=None):
    assert (path_dir is None) != (paths is None)

    if path_dir:
        paths = path_dir.iterdir()

    data = [pd.read_parquet(path_file) for path_file in paths]
    data = pd.concat(data, ignore_index=True, sort=True)

    return data
