import dagster

from aggregator.data_platform.raw.scraping.scraper import Scraper
from aggregator.data_platform.raw.scraping.url_generation.generator_date import UrlGeneratorWithDateState
from aggregator.data_platform.raw.scraping.url_generation.generator_int import UrlGeneratorWithIntState
from aggregator.data_platform.structured.medicine import StructuredEtlMedicine
from aggregator.data_platform.structured.naviny import StructuredEtlNaviny
from aggregator.data_platform.structured.tutby import StructuredEtlTutby


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
        'url_template': 'https://naviny.media/day/{}',
        'path_target': path_lake / path_target,
        'path_bad_data': path_lake / path_bad_data,
        'database': context.resources.database,
        'process_name': 'generator_naviny',
        'default_start_state': context.solid_config['default_start_state'],
    }

    UrlGeneratorWithDateState(**params).run()

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
        'max_n_fails': context.solid_config['max_n_fails'],
        'spark': context.resources.pyspark.spark_session,
        'url_template': 'https://news.tut.by/{}.html',
        'path_target': path_lake / path_target,
        'path_bad_data': path_lake / path_bad_data,
        'database': context.resources.database,
        'process_name': 'generator_tutby',
        'default_start_state': context.solid_config['default_start_state'],
    }

    UrlGeneratorWithIntState(**params).run()

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

    UrlGeneratorWithIntState(**params).run()

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

    UrlGeneratorWithIntState(**params).run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_scraper_tutby(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
        'database': context.resources.database,
        'process_name': 'scraper_tutby',
    }

    Scraper(**params).run()

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

    Scraper(**params).run()

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

    Scraper(**params).run()

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

    Scraper(**params).run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_structured_4gkb(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
        'database': context.resources.database,
        'process_name': 'structured_4gkb',
    }

    StructuredEtlMedicine(**params).run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_structured_komzdrav(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
        'database': context.resources.database,
        'process_name': 'structured_komzdrav',
    }

    StructuredEtlMedicine(**params).run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_structured_naviny(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
        'database': context.resources.database,
        'process_name': 'structured_naviny',
    }

    StructuredEtlNaviny(**params).run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_structured_tutby(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake / path_source,
        'path_target': path_lake / path_target,
        'database': context.resources.database,
        'process_name': 'structured_tutby',
    }

    StructuredEtlTutby(**params).run()

    return path_target
