from pathlib import Path

from staging.medicine import StagingEtlMedicine
from staging.tutby import StagingEtlTutby


def main():

    params = {
        'process_name': 'staging_medicine',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\landing\medicine_0'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\medicine_0'),
    }

    etl = StagingEtlMedicine(**params)
    etl.run()

    params = {
        'process_name': 'staging_medicine',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\landing\medicine_1'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\medicine_1'),
    }

    etl = StagingEtlMedicine(**params)
    etl.run()

    params = {
        'process_name': 'staging_tutby',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\landing\tutby'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\tutby'),
    }

    etl = StagingEtlTutby(**params)
    etl.run()


if __name__ == '__main__':
    main()
