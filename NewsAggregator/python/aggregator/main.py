from aggregator.analytics.clustering.run import main as main_clustering
from aggregator.analytics.embedding.postprocessing.run import main as main_umap
from aggregator.analytics.embedding.run import main as main_embedding
from aggregator.analytics.index.run import main as main_index
from aggregator.analytics.keywords.run import main as main_keywords
from aggregator.analytics.text_preprocessing.run import main as main_preprocessing
from aggregator.curated.run import main as main_curated
from aggregator.raw.scraping.run import main as main_scraping
from aggregator.raw.scraping.url_generation.run import main as main_generation
from aggregator.structured.run import main as main_structured


def main():
    main_generation()
    main_scraping()
    main_structured()
    main_curated()
    main_preprocessing()
    main_keywords()
    main_embedding()
    main_index()
    main_umap()
    main_clustering()


if __name__ == '__main__':
    main()
