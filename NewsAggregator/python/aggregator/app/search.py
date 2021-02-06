from pathlib import Path

import faiss
import numpy as np
import pandas as pd
import psycopg2
import streamlit as st

from aggregator.utils.function import read_parquet


# streamlit run aggregator/app/search.py


def main():

    index, data = get_data()

    st.title('Similarity search :mag: :newspaper: :heavy_check_mark:')

    option = st.selectbox('Article', data.to_numpy(), format_func=lambda record: record[1])

    embedding = option[5]
    embedding = embedding[np.newaxis, ...]
    embedding = embedding.astype(np.float32)

    distances, labels = index.search(embedding, k=6)

    distances = distances[0]
    labels = labels[0]

    for label, distance in zip(labels, distances):
        record = data[data['url_id'] == label].iloc[0]
        s = f"\[{record['time']}\] [{record['header']}]({record['url']}) (distance: {distance:.3f}, class: {record['label']})"
        st.info(s)


@st.cache(allow_output_mutation=True)
def get_data():
    path_index = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\index\index.faiss')
    path_articles = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\curated\articles')
    path_embeddings = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\embeddings')
    path_class = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\clustering')

    index = faiss.read_index(str(path_index))

    articles = read_parquet(path_articles)
    embeddings = read_parquet(path_embeddings)
    classes = read_parquet(path_class)

    articles = articles.set_index('url_id', drop=False)
    embeddings = embeddings.set_index('url_id')
    classes = classes.set_index('url_id')

    urls = get_urls(articles['url_id'])

    data = articles.join(embeddings, how='inner', rsuffix='_emb')
    data = data.join(classes, how='inner')
    data = data.join(urls, how='inner')

    data = data.sort_values('time', ascending=False)

    return index, data


def get_urls(url_ids):

    auditdb_url = '34.123.127.77'
    auditdb_name = 'dbaudit'
    user_name = 'postgres'
    user_password = 'P@ssw0rd'

    connection = psycopg2.connect(
        host=auditdb_url, database=auditdb_name,
        user=user_name, password=user_password
    )
    cursor = connection.cursor()

    url_ids = url_ids.astype(str)
    url_ids = ','.join(url_ids)
    query = f"select id, url from urls where id in ({url_ids});"
    cursor.execute(query)
    urls = cursor.fetchall()

    cursor.close()
    connection.close()

    urls = pd.DataFrame(urls, columns=('url_id', 'url'))
    urls = urls.set_index('url_id')

    return urls


if __name__ == '__main__':
    main()
