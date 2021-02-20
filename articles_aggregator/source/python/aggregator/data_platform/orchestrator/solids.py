import dagster

from aggregator.data_platform.raw.scraping.url_generation.generator_date import UrlGeneratorWithDateState
from aggregator.data_platform.raw.scraping.url_generation.generator_int import UrlGeneratorWithIntState


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_generator_tutby(context) -> None:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'source': 'tutby',
        'url_template': 'https://news.tut.by/{}.html',
        'default_start_state': '719730',
        'max_n_fails': 10,
        'path_target': path_lake / 'raw/urls/tutby.delta',
        'path_bad_data': path_lake / 'bad/urls.delta',
    }

    generator = UrlGeneratorWithIntState(**params)
    generator.run()


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_generator_naviny(context) -> None:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'source': 'naviny',
        'url_template': 'https://naviny.media/day/{}',
        'default_start_state': '2021/02/18',
        'path_target': path_lake / 'raw/urls/naviny.delta',
        'path_bad_data': path_lake / 'bad/urls.delta',
    }

    generator = UrlGeneratorWithDateState(**params)
    generator.run()
