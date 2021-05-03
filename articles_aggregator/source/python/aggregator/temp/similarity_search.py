from pathlib import Path

import faiss
import numpy as np

from aggregator.data_platform.utils import read_dir_parquet


# todo
if __name__ == '__main__':

    path_index = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\model\index\index.faiss')
    path_embeddings = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\embeddings')

    index = faiss.read_index(str(path_index))
    print(f'index length: {index.ntotal}')

    data = read_dir_parquet(path_embeddings)
    embeddings = data['document'].tolist()
    embeddings = np.array(embeddings, dtype=np.float32)
    embeddings = embeddings[:5]

    k = 4
    distances, labels = index.search(embeddings, k)
    print(labels)
    print(distances)
