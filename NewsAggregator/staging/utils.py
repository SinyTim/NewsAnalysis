from pathlib import Path
import psycopg2
import pandas as pd


def run(process_name, source, extract, columns, transform=None):
    path_landing = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\landing')
    path_staging = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging')

    path_landing = path_landing / source
    path_staging = path_staging / source
    path_staging.mkdir(exist_ok=True)

    connection = psycopg2.connect(host='127.0.0.1', database='auditdb',
                                  user='postgres', password='postgres')
    connection.autocommit = True
    cursor = connection.cursor()

    path_files = check_files(cursor, path_landing, process_name)

    if path_files:
        dfs = [pd.read_csv(path_file) for path_file in path_files]
        df = pd.concat(dfs, ignore_index=True)

        name_file = f"{df['url_id'].min()}_{df['url_id'].max()}.csv"
        path_destination = path_staging / name_file

        audit_ids = start(cursor, path_files, path_destination, process_name)

        data = df['html'].map(extract)

        index = data[data.map(len) != len(columns)].index
        bad_data = pd.concat((df['url_id'].loc[index], data.loc[index].str[1]), axis=1)

        data = data.apply(pd.Series)
        data.columns = columns
        df = pd.concat((df, data), axis=1)
        df = df.drop('html', axis=1)
        df = df.drop(index)

        if transform:
            df = transform(df)

        df.to_csv(path_destination, index=False)

        if len(bad_data) != 0:
            write_bad_data(cursor, bad_data)

        stop(cursor, audit_ids)

    if connection:
        cursor.close()
        connection.close()


def check_files(cursor, path_landing, process_name):
    path_files = {str(path_file) for path_file in path_landing.iterdir()}

    query = f"select source from audit where process_name = '{process_name}' and stop_time is not null;"
    cursor.execute(query)
    path_processed_files = cursor.fetchall()
    path_processed_files = {path_processed_file[0] for path_processed_file in path_processed_files}

    path_files -= path_processed_files

    return path_files


def write_bad_data(cursor, bad_data):
    values = bad_data.apply(lambda row: f"({row['url_id']},'{row['html']}')", axis=1)
    values = ','.join(values)
    query = f'insert into bad_data (url_id, error) values {values};'
    cursor.execute(query)


def start(cursor, path_files, path_destination, process_name):
    query = []
    for path_file in path_files:
        query += [f"('{path_file}','{path_destination}','{process_name}')"]

    query = ','.join(query)
    query = f"insert into audit (source, destination, process_name) values {query} returning id;"
    cursor.execute(query)
    audit_ids = cursor.fetchall()
    audit_ids = [str(_[0]) for _ in audit_ids]
    audit_ids = ','.join(audit_ids)
    audit_ids = f'({audit_ids})'
    return audit_ids


def stop(cursor, audit_ids):
    query = f'update audit set stop_time = now() where id in {audit_ids};'
    cursor.execute(query)
