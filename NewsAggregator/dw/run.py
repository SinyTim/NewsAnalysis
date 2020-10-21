from pathlib import Path

from dw.stage_to_dw_etl import StageToDwEtl


def main():

    params = [
        {
            'process_name': 'stage_to_dw',
            'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\medicine_0'),
            'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\documents_data'),
        },
        {
            'process_name': 'stage_to_dw',
            'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\medicine_1'),
            'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\documents_data'),
        },
        {
            'process_name': 'stage_to_dw',
            'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\tutby'),
            'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\documents_data'),
        },
    ]

    for param in params:
        etl = StageToDwEtl(**param)
        etl.run()


if __name__ == '__main__':
    main()
