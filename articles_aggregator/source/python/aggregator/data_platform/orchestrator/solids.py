import dagster

from aggregator.data_platform.raw.scraping.scraper import Scraper
from aggregator.data_platform.raw.scraping.url_generation.generator_date import UrlGeneratorWithDateState
from aggregator.data_platform.raw.scraping.url_generation.generator_int import UrlGeneratorWithIntState


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'default_start_state': dagster.Field(str, is_required=False, default_value='2021/02/18')
    },
)
def solid_generator_naviny(context, path_target: str, path_bad_data: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'process_name': 'generator_naviny',
        'url_template': 'https://naviny.media/day/{}',
        'default_start_state': context.solid_config['default_start_state'],
        'path_target': path_lake / path_target,
        'path_bad_data': path_lake / path_bad_data,
    }

    generator = UrlGeneratorWithDateState(**params)
    generator.run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'default_start_state': dagster.Field(str, is_required=False, default_value='719738'),
        'max_n_fails': dagster.Field(int, is_required=False, default_value=10),
    },
)
def solid_generator_tutby(context, path_target: str, path_bad_data: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'process_name': 'generator_tutby',
        'url_template': 'https://news.tut.by/{}.html',
        'default_start_state': context.solid_config['default_start_state'],
        'max_n_fails': context.solid_config['max_n_fails'],
        'path_target': path_lake / path_target,
        'path_bad_data': path_lake / path_bad_data,
    }

    generator = UrlGeneratorWithIntState(**params)
    generator.run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'default_start_state': dagster.Field(str, is_required=False, default_value='1'),
        'max_n_fails': dagster.Field(int, is_required=False, default_value=5),
    },
)
def solid_generator_komzdrav(context, path_target: str, path_bad_data: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'process_name': 'generator_komzdrav',
        'url_template': 'https://komzdrav-minsk.gov.by/news/{}',
        'default_start_state': context.solid_config['default_start_state'],
        'max_n_fails': context.solid_config['max_n_fails'],
        'path_target': path_lake / path_target,
        'path_bad_data': path_lake / path_bad_data,
    }

    generator = UrlGeneratorWithIntState(**params)
    generator.run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'default_start_state': dagster.Field(str, is_required=False, default_value='1'),
        'max_n_fails': dagster.Field(int, is_required=False, default_value=35),
    },
)
def solid_generator_4gkb(context, path_target: str, path_bad_data: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'process_name': 'generator_4gkb',
        'url_template': 'https://4gkb.by/news/{}',
        'default_start_state': context.solid_config['default_start_state'],
        'max_n_fails': context.solid_config['max_n_fails'],
        'path_target': path_lake / path_target,
        'path_bad_data': path_lake / path_bad_data,
    }

    generator = UrlGeneratorWithIntState(**params)
    generator.run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_scraper_tutby(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'process_name': 'scraper_tutby',
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
    }

    generator = Scraper(**params)
    generator.run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_scraper_naviny(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'process_name': 'scraper_naviny',
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
    }

    generator = Scraper(**params)
    generator.run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_scraper_komzdrav(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'process_name': 'scraper_komzdrav',
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
    }

    generator = Scraper(**params)
    generator.run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_scraper_4gkb(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'database': context.resources.database,
        'process_name': 'scraper_4gkb',
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
    }

    generator = Scraper(**params)
    generator.run()

    return path_target
