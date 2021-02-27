import requests
from bs4 import BeautifulSoup
from pyspark.sql.functions import col
from pyspark.sql.functions import udf

from aggregator.data_platform.utils.incremental_delta_etl import IncrementalDeltaEtl


class Scraper(IncrementalDeltaEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transform(self, df_urls):

        get_html = udf(self.get_html)
        get_body = udf(self.get_body)

        # todo set number of executors instead of repartition
        df_html = df_urls \
            .repartition(2) \
            .withColumn('html', get_html('url')) \
            .withColumn('html', get_body('html')) \
            .select(col('id').alias('url_id'), 'html')

        return df_html

    @staticmethod
    def get_html(url: str):
        response = requests.get(url)
        html = response.text
        return html

    @staticmethod
    def get_body(page: str):
        soup = BeautifulSoup(page, 'html.parser')
        body = str(soup.body)
        return body
