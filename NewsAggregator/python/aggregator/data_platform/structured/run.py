from pathlib import Path

from aggregator.data_platform.structured.medicine import StructuredEtlMedicine
from aggregator.data_platform.structured.naviny import StructuredEtlNaviny
from aggregator.data_platform.structured.tutby import StructuredEtlTutby


def main():

    params = {
        'process_name': 'structured_medicine',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\raw\4gkb'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\structured\4gkb'),
    }

    etl = StructuredEtlMedicine(**params)
    etl.run()

    params = {
        'process_name': 'structured_medicine',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\raw\komzdrav'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\structured\komzdrav'),
    }

    etl = StructuredEtlMedicine(**params)
    etl.run()

    params = {
        'process_name': 'structured_tutby',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\raw\tutby'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\structured\tutby'),
    }

    etl = StructuredEtlTutby(**params)
    etl.run()

    params = {
        'process_name': 'structured_naviny',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\raw\naviny'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\structured\naviny'),
    }

    etl = StructuredEtlNaviny(**params)
    etl.run()


if __name__ == '__main__':
    main()
