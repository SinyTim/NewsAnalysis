from pathlib import Path

import faiss
import numpy as np

from utils.function import read_dir_parquet


if __name__ == '__main__':

    path_embeddings = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\dw\embeddings')
    path_index = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\index\index.faiss')

    data = read_dir_parquet(path_embeddings)

    embeddings = data['document'].tolist()
    embeddings = np.array(embeddings, dtype=np.float32)
    labels = data['url_id'].to_numpy()
    dim = embeddings.shape[1]

    index = faiss.index_factory(dim, 'IDMap,L2norm,Flat')
    index.add_with_ids(embeddings, labels)
    faiss.write_index(index, str(path_index))
