from pathlib import Path

from text_preprocessing.preprocessing_etl import PreprocessingEtl


def main():

    params = {
        'process_name': 'text_preprocessing',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\documents_data'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\preprocessed'),
    }

    etl = PreprocessingEtl(**params)
    etl.run()


if __name__ == '__main__':
    main()
