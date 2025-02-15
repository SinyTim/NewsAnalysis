import requests
from bs4 import BeautifulSoup
from pyspark.sql.functions import col
from pyspark.sql.functions import udf

from aggregator.data_platform.utils.etls.incremental_delta_etl import IncrementalDeltaEtl


class Scraper(IncrementalDeltaEtl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transform(self, df_urls):

        size_partition = 10000
        n_urls = df_urls.count()
        n_partitions = n_urls // size_partition
        n_partitions = max(n_partitions, 1)

        # todo set 1 executor with 2 cores
        df_html = df_urls \
            .repartition(n_partitions) \
            .withColumn('html', get_html('url')) \
            .withColumn('html', get_body('html')) \
            .select(col('id').alias('url_id'), 'html')

        return df_html


@udf
def get_html(url: str) -> str:
    response = requests.get(url)
    html = response.text
    return html


@udf
def get_body(page: str) -> str:
    soup = BeautifulSoup(page, 'html.parser')
    body = str(soup.body)
    return body
