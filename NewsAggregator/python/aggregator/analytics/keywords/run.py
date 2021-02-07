from pathlib import Path

from aggregator.analytics.keywords.keyword_etl import KeywordEtl


def main():

    params = {
        'process_name': 'keywords',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\preprocessed'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\keywords'),
        'path_idf': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\idf\idf.csv'),
    }

    etl = KeywordEtl(**params)
    etl.run()


if __name__ == '__main__':
    main()
