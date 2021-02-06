from pathlib import Path

from aggregator.analytics.clustering.clustering_etl import ClusteringEtl


def main():

    params = {
        'process_name': 'clustering',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\postprocessing_umap'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\clustering'),
    }

    etl = ClusteringEtl(**params)
    etl.run()


if __name__ == '__main__':
    main()
