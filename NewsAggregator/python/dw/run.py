from pathlib import Path

from dw.stage_to_dw_etl import StageToDwEtl


def main():

    process_name = 'stage_to_dw'
    path_sources = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging')
    path_destination = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\documents_data')

    for path_source in path_sources.iterdir():

        params = {
            'process_name': process_name,
            'path_source': path_source,
            'path_destination': path_destination,
        }

        etl = StageToDwEtl(**params)
        etl.run()


if __name__ == '__main__':
    main()
