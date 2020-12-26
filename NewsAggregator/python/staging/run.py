from pathlib import Path

from staging.medicine import StagingEtlMedicine
from staging.naviny import StagingEtlNaviny
from staging.tutby import StagingEtlTutby


def main():

    params = {
        'process_name': 'staging_medicine',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\landing\4gkb'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\4gkb'),
    }

    etl = StagingEtlMedicine(**params)
    etl.run()

    params = {
        'process_name': 'staging_medicine',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\landing\komzdrav'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\komzdrav'),
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

    params = {
        'process_name': 'staging_naviny',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\landing\naviny'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\staging\naviny'),
    }

    etl = StagingEtlNaviny(**params)
    etl.run()


if __name__ == '__main__':
    main()
