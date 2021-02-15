from aggregator.data_platform.analytics.clustering.run import main as main_clustering
from aggregator.data_platform.analytics.embedding.postprocessing.run import main as main_umap
from aggregator.data_platform.analytics.embedding.run import main as main_embedding
from aggregator.data_platform.analytics.index.run import main as main_index
from aggregator.data_platform.analytics.keywords.run import main as main_keywords
from aggregator.data_platform.analytics.text_preprocessing.run import main as main_preprocessing
from aggregator.data_platform.analytics.topicwords.run import main as main_topicwords
from aggregator.data_platform.curated.run import main as main_curated
from aggregator.data_platform.raw.scraping.run import main as main_scraping
from aggregator.data_platform.raw.scraping.url_generation.run import main as main_generation
from aggregator.data_platform.structured.run import main as main_structured


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
    main_topicwords()


if __name__ == '__main__':
    main()
