from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# streamlit run aggregator/front/topic.py


def main():
    st.title('Topic modeling :mag: :newspaper: :heavy_check_mark:')

    df_topics, df_frequencies, df_article_topic = get_data()

    topic_id = get_topic_id(df_topics)

    if topic_id:
        write_plot(df_frequencies, topic_id)
        write_articles(df_article_topic, topic_id)
    else:
        write_plot_entire(df_topics, df_frequencies)


@st.cache(allow_output_mutation=False)
def get_data():

    path_lake = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\articles_aggregator\data\_data')

    path_topics = path_lake / Path('consumer/topics.parquet')
    path_frequencies = path_lake / Path('consumer/frequencies.parquet')
    path_article_topic = path_lake / Path('consumer/article_topic.parquet')

    df_topics = pd.read_parquet(path_topics)
    df_frequencies = pd.read_parquet(path_frequencies)
    df_article_topic = pd.read_parquet(path_article_topic)

    return df_topics, df_frequencies, df_article_topic


def get_topic_id(df_topics):

    n_articles = df_topics['topic_size'].sum()
    df_topics = df_topics.to_numpy()
    df_topics = np.insert(df_topics, 0, values=[None, n_articles, ['All']], axis=0)

    format_func = lambda record: ', '.join(record[2]) + f' ({record[1]})'
    option = st.selectbox('Topic', df_topics, format_func=format_func)

    topic_id = option[0]

    return topic_id


def write_plot_entire(df_topics, df_frequencies):

    topic_ids = df_topics['topic_id']

    figure = go.Figure()

    for topic_id in topic_ids:
        df_topic_frequencies = df_frequencies[df_frequencies['topic_id'] == topic_id]

        max_change = df_topic_frequencies['frequency'].max() - df_topic_frequencies['frequency'].min()

        if max_change > 0.06:
            topic_words = df_topics[df_topics['topic_id'] == topic_id]['topic_words'].iloc[0]
            topic_words = topic_words[:3]
            topic_words = ', '.join(topic_words)
            figure.add_scatter(x=df_topic_frequencies['time'], y=df_topic_frequencies['frequency'],
                               mode='lines', name=topic_words)

    figure.update_yaxes(title_text='% of all articles')
    st.plotly_chart(figure, use_container_width=True)


def write_plot(df_frequencies, topic_id):

    df_topic_frequencies = df_frequencies[df_frequencies['topic_id'] == topic_id]

    figure = go.Figure()
    figure.add_scatter(x=df_topic_frequencies['time'], y=df_topic_frequencies['frequency'],
                       mode='lines')
    figure.update_yaxes(title_text='% of all articles')
    st.plotly_chart(figure, use_container_width=True)


def write_articles(df_article_topic, topic_id):

    df_topic = df_article_topic[df_article_topic['topic_id'] == topic_id]

    df_topic = df_topic \
        .sort_values('time', ascending=False) \
        .head(7)

    for record in df_topic.itertuples():
        tags = ', '.join(record.tags)
        tags = f'({tags})' if tags else ''
        s = fr"_\[{record.Index}\]_ **{record.header}** {tags}"
        st.info(s)


if __name__ == '__main__':
    main()
