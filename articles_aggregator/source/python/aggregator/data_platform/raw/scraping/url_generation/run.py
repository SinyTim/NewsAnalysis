import logging
from pathlib import Path

from pyspark.sql import SparkSession

from aggregator.data_platform.raw.scraping.url_generation.generator_date import UrlGeneratorWithDateState
from aggregator.data_platform.raw.scraping.url_generation.generator_int import UrlGeneratorWithIntState


def main():
    logging.basicConfig(level=logging.INFO)

    spark = SparkSession.builder \
        .config('spark.jars.packages', 'io.delta:delta-core_2.12:0.8.0') \
        .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
        .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
        .getOrCreate()

    path_target = Path(r'file://C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\raw\urls')
    path_bad_data = Path(r'file://C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\bad\urls.delta')

    params_base = {
        'spark': spark,
        'path_bad_data': path_bad_data,
    }

    params = [
        {
            'source': 'komzdrav',
            'url_template': 'https://komzdrav-minsk.gov.by/news/{}',
            'default_start_state': '1',
            'max_n_fails': 5,
            'path_target': path_target / 'komzdrav.delta',
        },
        {
            'source': '4gkb',
            'url_template': 'https://4gkb.by/news/{}',
            'default_start_state': '1',
            'max_n_fails': 35,
            'path_target': path_target / '4gkb.delta',
        },
        {
            'source': 'tutby',
            'url_template': 'https://news.tut.by/{}.html',
            'default_start_state': '717000',
            'max_n_fails': 10,
            'path_target': path_target / 'tutby.delta',
        },
    ]

    for param in params:
        generator = UrlGeneratorWithIntState(**param, **params_base)
        generator.run()

    params = {
        'source': 'naviny',
        'url_template': 'https://naviny.media/day/{}',
        'default_start_state': '2021/01/28',
        'spark': spark,
        'path_bad_data': path_bad_data,
        'path_target': path_target / 'naviny.delta',
    }

    generator = UrlGeneratorWithDateState(**params)
    generator.run()


if __name__ == '__main__':
    main()
