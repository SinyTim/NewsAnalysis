from pathlib import Path

import dagster

from aggregator.data_platform.analytics.clustering.clustering_etl import ClusteringEtl
from aggregator.data_platform.analytics.embedding.postprocessing.umap_etl import UmapEtl
from aggregator.data_platform.analytics.embedding.word2vec_etl import Word2vecEtl
from aggregator.data_platform.analytics.text_preprocessing.preprocessing_etl import PreprocessingEtl
from aggregator.data_platform.analytics.topicwords.topic_keyword_etl import TopicKeywordEtl
from aggregator.data_platform.curated.structured_to_curated_etl import StructuredToCuratedEtl
from aggregator.data_platform.raw.scraping.scraper import Scraper
from aggregator.data_platform.raw.scraping.url_generation.generator_date import UrlGeneratorWithDateState
from aggregator.data_platform.raw.scraping.url_generation.generator_int import UrlGeneratorWithIntState
from aggregator.data_platform.structured.medicine import StructuredEtlMedicine
from aggregator.data_platform.structured.naviny import StructuredEtlNaviny
from aggregator.data_platform.structured.tutby import StructuredEtlTutby
from aggregator.data_platform.consumer.export_etl import ExportEtl


@dagster.solid(required_resource_keys={'pyspark_step_launcher', 'pyspark'})
def solid_export(context, path_source: str, path_target: str) -> str:

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_source,
        'path_target': path_target,
    }

    ExportEtl(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'default_start_state': dagster.Field(str, is_required=True)
    },
)
def solid_generator_naviny(context, path_target: str, path_bad_data: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'url_template': 'https://naviny.online/day/{}',
        'path_target': path_lake + path_target,
        'path_bad_data': path_lake + path_bad_data,
        'database': context.resources.database,
        'process_name': 'generator_naviny',
        'default_start_state': context.solid_config['default_start_state'],
    }

    UrlGeneratorWithDateState(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'default_start_state': dagster.Field(str, is_required=True),
        'max_n_fails': dagster.Field(int, is_required=True),
    },
)
def solid_generator_tutby(context, path_target: str, path_bad_data: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'max_n_fails': context.solid_config['max_n_fails'],
        'spark': context.resources.pyspark.spark_session,
        'url_template': 'https://news.tut.by/{}.html',
        'path_target': path_lake + path_target,
        'path_bad_data': path_lake + path_bad_data,
        'database': context.resources.database,
        'process_name': 'generator_tutby',
        'default_start_state': context.solid_config['default_start_state'],
    }

    UrlGeneratorWithIntState(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'default_start_state': dagster.Field(str, is_required=True),
        'max_n_fails': dagster.Field(int, is_required=True),
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
        'path_target': path_lake + path_target,
        'path_bad_data': path_lake + path_bad_data,
    }

    UrlGeneratorWithIntState(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'default_start_state': dagster.Field(str, is_required=True),
        'max_n_fails': dagster.Field(int, is_required=True),
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
        'path_target': path_lake + path_target,
        'path_bad_data': path_lake + path_bad_data,
    }

    UrlGeneratorWithIntState(**params).run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_scraper_tutby(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
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
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
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
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
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
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
    }

    Scraper(**params).run()

    return path_target


@dagster.solid(required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'})
def solid_structured_4gkb(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
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
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
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
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
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
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
        'database': context.resources.database,
        'process_name': 'structured_tutby',
    }

    StructuredEtlTutby(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'process_name': dagster.Field(str, is_required=True),
    },
)
def solid_curated(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
        'database': context.resources.database,
        'process_name': context.solid_config['process_name'],
    }

    StructuredToCuratedEtl(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'process_name': dagster.Field(str, is_required=True),
    },
)
def solid_preprocessing(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
        'database': context.resources.database,
        'process_name': context.solid_config['process_name'],
    }

    PreprocessingEtl(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'process_name': dagster.Field(str, is_required=True),
        'path_word2vec': dagster.Field(str, is_required=True),
        'path_idf': dagster.Field(str, is_required=True),
    },
)
def solid_word2vec(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'path_word2vec': Path(path_lake + context.solid_config['path_word2vec']).as_posix().replace('file:/', ''),
        'path_idf': Path(path_lake + context.solid_config['path_idf']).as_posix().replace('file:/', ''),
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
        'database': context.resources.database,
        'process_name': context.solid_config['process_name'],
    }

    Word2vecEtl(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'database', 'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'process_name': dagster.Field(str, is_required=True),
        'path_umap': dagster.Field(str, is_required=True),
    },
)
def solid_umap(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'path_umap': Path(path_lake + context.solid_config['path_umap']).as_posix().replace('file:/', ''),
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
        'database': context.resources.database,
        'process_name': context.solid_config['process_name'],
    }

    UmapEtl(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'datalake', 'pyspark_step_launcher', 'pyspark'},
)
def solid_clustering(context, path_source: str, path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source': path_lake + path_source,
        'path_target': path_lake + path_target,
    }

    ClusteringEtl(**params).run()

    return path_target


@dagster.solid(
    required_resource_keys={'datalake', 'pyspark_step_launcher', 'pyspark'},
    config_schema={
        'path_idf': dagster.Field(str, is_required=True),
    },
)
def solid_topicwords(context,
                     path_source_topic_ids: str,
                     path_source_documents: str,
                     path_target: str) -> str:

    path_lake = context.resources.datalake

    params = {
        'spark': context.resources.pyspark.spark_session,
        'path_source_topic_ids': path_lake + path_source_topic_ids,
        'path_source_documents': path_lake + path_source_documents,
        'path_target': path_lake + path_target,
        'path_idf': Path(path_lake + context.solid_config['path_idf']).as_posix().replace('file:/', ''),
    }

    TopicKeywordEtl(**params).run()

    return path_target
