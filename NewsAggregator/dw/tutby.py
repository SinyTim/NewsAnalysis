from pathlib import Path
import pandas as pd


def main():
    source = 'tutby'

    path_staging = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging')
    path_dw = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\documents_data')

    path_staging = path_staging / source
    path_staging.mkdir(exist_ok=True)
    name_file = f'{source}.parquet'
    path_dw = path_dw / name_file

    path_files = list(path_staging.iterdir())

    dfs = [pd.read_csv(path, parse_dates=True, infer_datetime_format=True) for path in path_files]
    df = pd.concat(dfs, ignore_index=True)

    df = df[['url_id', 'header', 'time', 'document', 'tags']]

    df.to_parquet(path_dw, index=False)


if __name__ == '__main__':
    main()
