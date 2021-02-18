from pathlib import Path

from pyspark.sql import SparkSession

from aggregator.data_platform.raw.scraping.scraper import Scraper


class ScraperS(Scraper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.spark = SparkSession.builder.getOrCreate()

    def extract(self, source):
        df = self.spark.createDataFrame(source, schema=['url_id', 'url', 'source_site'])
        exit()

    def transform(self, data):
        pass

    def load(self, data, destination):
        pass # partition by source cite


if __name__ == '__main__':
    params = {
        'process_name': 'scraper',
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\raw'),
    }
    ScraperS(**params).run()
