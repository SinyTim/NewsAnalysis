from pathlib import Path

from aggregator.analytics.index.index_etl import IndexEtl


def main():

    params = {
        'process_name': 'index',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\embeddings'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\index'),
    }

    etl = IndexEtl(**params)
    etl.run()


if __name__ == '__main__':
    main()
