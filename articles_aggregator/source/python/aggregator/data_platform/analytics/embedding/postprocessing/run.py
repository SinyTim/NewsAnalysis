from pathlib import Path

from aggregator.data_platform.analytics.embedding.postprocessing.umap_etl import UmapEtl


def main():

    params = {
        'process_name': 'umap',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\embeddings'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\postprocessing_umap'),
        'path_umap': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\umap\umap.pickle'),
    }

    etl = UmapEtl(**params)
    etl.run()


if __name__ == '__main__':
    main()
