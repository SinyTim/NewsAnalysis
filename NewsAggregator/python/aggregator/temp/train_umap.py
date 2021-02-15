import pickle
from pathlib import Path

import numpy as np
import umap


def main():

    path_embeddings = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\emb\emb_clean_tutby_126784_w2v_idf.npy')
    # path_embeddings = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\analytics\embeddings')
    path_umap = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\models\umap\umap.pickle')

    with open(path_embeddings, 'rb') as file:
        embeddings = np.load(file)
        index = ~np.isnan(embeddings).any(axis=1)
        embeddings = embeddings[index]

    # data = read_parquet(path_embeddings)
    # embeddings = data['document'].to_list()
    # embeddings = np.array(embeddings, dtype=np.float32)

    umap_model = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine')

    umap_model.fit(embeddings)

    with open(path_umap, 'wb') as file:
        pickle.dump(umap_model, file)


if __name__ == '__main__':
    main()
