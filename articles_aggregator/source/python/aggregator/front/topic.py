from pathlib import Path

import streamlit as st

from aggregator.front import search
from aggregator.data_platform.utils.function import read_parquet


# streamlit run aggregator/app/topic.py


def main():

    topicwords, data = get_data()

    st.title('Topic modeling :mag: :newspaper: :heavy_check_mark:')

    option = st.selectbox('Topic', topicwords.to_numpy(), format_func=lambda record: ', '.join(record[1]))

    topic_id = option[0]

    data_topic = data[data['topic_id'] == topic_id]
    data_topic = data_topic.sort_values('time', ascending=False)
    data_topic = data_topic.head(20)

    for record in data_topic.itertuples():
        s = fr"\[{record.time}\] [{record.header}]({record.url})"
        st.info(s)


@st.cache(allow_output_mutation=True)
def get_data():
    path_articles = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\curated\articles')
    path_topics = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\clustering')
    path_topicwords = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\topicwords')

    articles = read_parquet(path_articles)
    topics = read_parquet(path_topics)
    topicwords = read_parquet(path_topicwords)
    urls = search.get_urls(articles['url_id'])

    articles = articles.set_index('url_id', drop=False)
    topics = topics.set_index('url_id')

    data = articles.join(topics, how='inner')
    data = data.join(urls, how='inner')

    data = data.sort_values('time', ascending=False)

    return topicwords, data


if __name__ == '__main__':
    main()
