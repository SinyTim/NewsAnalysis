from pathlib import Path

from aggregator.data_platform.analytics.topicwords.topic_keyword_etl import TopicKeywordEtl


def main():

    params = {
        'process_name': 'keywords',
        'path_documents': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\preprocessed'),
        'path_topic_ids': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\clustering'),
        'path_idf': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\idf\idf.csv'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\topicwords'),
    }

    etl = TopicKeywordEtl(**params)
    etl.run()


if __name__ == '__main__':
    main()
