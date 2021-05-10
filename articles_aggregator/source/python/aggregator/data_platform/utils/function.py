import uuid
from pathlib import Path

import pandas as pd


def read_delta(spark, path):
    return spark.read \
        .format('delta') \
        .load(str(path))


def write_delta(df, path, mode='append', name_column_partition=None):

    writer = df.write \
        .format('delta')

    if name_column_partition:
        writer = writer.partitionBy(name_column_partition)

    writer \
        .mode(mode) \
        .save(str(path))


def write_csv(df, path):
    df.write \
        .format('com.databricks.spark.csv') \
        .mode('overwrite') \
        .option('header', 'true') \
        .option('delimiter', ',') \
        .save(path)


def write_json(df, path):
    df.write \
        .format('json') \
        .mode('overwrite') \
        .save(path)


def read_parquet(path_dir: Path = None, paths=None):
    assert (path_dir is None) != (paths is None)

    if path_dir:
        paths = path_dir.iterdir()

    data = [pd.read_parquet(path_file) for path_file in paths]
    data = pd.concat(data, ignore_index=True, sort=True)

    return data


def add_id_column(df):
    id_prefix = uuid.uuid1()
    df['id'] = [f'{id_prefix}-{index}' for index in range(len(df))]
    return df
