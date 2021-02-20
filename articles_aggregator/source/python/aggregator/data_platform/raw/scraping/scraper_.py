from pathlib import Path

import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf

from aggregator.data_platform.raw.scraping.scraper import Scraper


class ScraperS(Scraper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.spark = SparkSession.builder.getOrCreate()

    def extract(self, source):
        df_source = self.spark.createDataFrame(source, schema=['url_id', 'url', 'source_site'])
        get_html = udf(lambda url: requests.get(url).text)
        get_body = udf(self.get_body)
        df = df_source \
            .repartition(2) \
            .withColumn('html', get_html('url')) \
            .withColumn('html', get_body('html'))
        exit()

    def transform(self, data):
        pass

    def load(self, data, destination):
        pass


if __name__ == '__main__':
    params = {
        'process_name': 'scraper',
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\raw'),
    }
    ScraperS(**params).run()
