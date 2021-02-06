from pathlib import Path

from aggregator.curated.structured_to_curated_etl import StructuredToCuratedEtl


def main():

    process_name = 'structured_to_curated'
    path_sources = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\structured')
    path_destination = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\curated\articles')

    for path_source in path_sources.iterdir():

        params = {
            'process_name': process_name,
            'path_source': path_source,
            'path_destination': path_destination,
        }

        etl = StructuredToCuratedEtl(**params)
        etl.run()


if __name__ == '__main__':
    main()
