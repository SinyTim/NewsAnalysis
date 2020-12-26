from pathlib import Path

from embedding.inference_word2vec import Word2vecEtl


def main():

    params = {
        'process_name': 'word2vec',
        'path_source': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\preprocessed'),
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\embeddings'),
        'path_word2vec': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\model\w2v\model_w2v_clean_tutby_126784.model'),
        'path_idf': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\idf.csv'),
    }

    etl = Word2vecEtl(**params)
    etl.run()


if __name__ == '__main__':
    main()
