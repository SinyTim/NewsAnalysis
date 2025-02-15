import os

import dagster
import dagster_pyspark
from dagster.core.definitions.no_step_launcher import no_step_launcher

from aggregator.data_platform.orchestrator import resources
from aggregator.data_platform.orchestrator import solids


# os.environ['PYSPARK_PYTHON'] = './environment/bin/python'


mode_local = dagster.ModeDefinition(
    name='local',
    resource_defs={
        'database': resources.postgres_database,
        'datalake': resources.datalake,
        'pyspark_step_launcher': no_step_launcher,
        'pyspark': dagster_pyspark.pyspark_resource.configured({'spark_conf': {
            'spark.submit.pyFiles': dagster.file_relative_path(
                __file__, '../../../../../packages/articles_aggregator-0.0.0-py3-none-any.whl'),
            # 'spark.archives': dagster.file_relative_path(
            #     __file__, '../../../../../packages/pyspark_conda_env.tar.gz#environment'),
            'spark.jars.packages': 'io.delta:delta-core_2.12:0.8.0',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
            'spark.sql.catalog.spark_catalog': 'org.apache.spark.sql.delta.catalog.DeltaCatalog',
            'spark.sql.adaptive.enabled': 'true',
            'spark.sql.execution.arrow.pyspark.enabled': 'true',
            'spark.sql.execution.arrow.maxRecordsPerBatch': 1000,  # because of text preprocessing job.
            # 'spark.default.parallelism': 8,
            'spark.jars': r'C:\Users\Tim\Programs\spark\gcs-connector-hadoop3-latest.jar',
            'spark.hadoop.fs.gs.impl': 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem',
            'spark.hadoop.fs.AbstractFileSystem.gs.impl': 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS',
            'spark.hadoop.google.cloud.auth.service.account.enable': 'true',
            'spark.hadoop.google.cloud.auth.service.account.json.keyfile':
                dagster.file_relative_path(__file__, '../../../../../configs/gcs_keyfile.json'),
            # 'spark.executor.instances': 1,
            # 'spark.executor.cores': 2,
            # 'spark.executor.memory': '1g',
            'spark.driver.memory': '8g',
        }}),
    }
)

mode_dataproc = dagster.ModeDefinition(
    name='dataproc',
    resource_defs={
        'database': resources.postgres_database,
        'datalake': resources.datalake,
        'pyspark_step_launcher': no_step_launcher,
        'pyspark': dagster_pyspark.pyspark_resource.configured({'spark_conf': {
            'spark.submit.pyFiles': dagster.file_relative_path(
                __file__, '../../../../../packages/articles_aggregator-0.0.0-py3-none-any.whl'),
            'spark.archives': dagster.file_relative_path(
                __file__, '../../../../../packages/pyspark_conda_env.tar.gz#environment'),
            # 'spark.pyspark.driver.python': 'python',
            # 'spark.pyspark.python': './environment/bin/python',
            'spark.jars.packages': 'io.delta:delta-core_2.12:0.8.0',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
            'spark.sql.catalog.spark_catalog': 'org.apache.spark.sql.delta.catalog.DeltaCatalog',
            'spark.sql.execution.arrow.pyspark.enabled': 'true',
            'spark.sql.execution.arrow.maxRecordsPerBatch': 10000,
            # 'spark.default.parallelism': 8,
        }}),
    }
)


preset_dev = dagster.PresetDefinition.from_files(
    name='dev',
    config_files=[
        dagster.file_relative_path(__file__, '../../../../../configs/config_dev_db.yaml'),
        dagster.file_relative_path(__file__, '../../../../../configs/config_dev_lake.yaml'),
        dagster.file_relative_path(__file__, '../../../../../configs/config_pipe.yaml'),
    ],
    mode='local',
)


preset_prod = dagster.PresetDefinition.from_files(
    name='prod',
    config_files=[
        dagster.file_relative_path(__file__, '../../../../../configs/config_prod_db.yaml'),
        dagster.file_relative_path(__file__, '../../../../../configs/config_prod_lake.yaml'),
        dagster.file_relative_path(__file__, '../../../../../configs/config_pipe.yaml'),
    ],
    mode='dataproc',
)


preset_export = dagster.PresetDefinition.from_files(
    name='export',
    config_files=[
        dagster.file_relative_path(__file__, '../../../../../configs/config_export.yaml'),
    ],
    mode='local',
)


@dagster.composite_solid
def composite_curated() -> str:

    # path_url_naviny = solids.solid_generator_naviny()
    path_url_tutby = solids.solid_generator_tutby()
    path_url_komzdrav = solids.solid_generator_komzdrav()
    path_url_4gkb = solids.solid_generator_4gkb()

    # path_html_naviny = solids.solid_scraper_naviny(path_source=path_url_naviny)
    path_html_tutby = solids.solid_scraper_tutby(path_source=path_url_tutby)
    path_html_komzdrav = solids.solid_scraper_komzdrav(path_source=path_url_komzdrav)
    path_html_4gkb = solids.solid_scraper_4gkb(path_source=path_url_4gkb)

    # path_structured_naviny = solids.solid_structured_naviny(path_source=path_html_naviny)
    path_structured_tutby = solids.solid_structured_tutby(path_source=path_html_tutby)
    path_structured_4gkb = solids.solid_structured_4gkb(path_source=path_html_4gkb)
    path_structured_komzdrav = solids.solid_structured_komzdrav(path_source=path_html_komzdrav)

    # solid_curated_naviny = solids.solid_curated.alias('solid_curated_naviny')
    solid_curated_tutby = solids.solid_curated.alias('solid_curated_tutby')
    solid_curated_4gkb = solids.solid_curated.alias('solid_curated_4gkb')
    solid_curated_komzdrav = solids.solid_curated.alias('solid_curated_komzdrav')
    # path_curated = solid_curated_naviny(path_source=path_structured_naviny)
    path_curated = solid_curated_tutby(path_source=path_structured_tutby)
    path_curated = solid_curated_4gkb(path_source=path_structured_4gkb)
    path_curated = solid_curated_komzdrav(path_source=path_structured_komzdrav)

    return path_curated


@dagster.composite_solid
def composite_analytics(path_curated: str):

    path_preprocessed = solids.solid_preprocessing(path_source=path_curated)
    path_embeddings = solids.solid_word2vec(path_source=path_preprocessed)
    path_umap = solids.solid_umap(path_source=path_embeddings)
    path_clustering = solids.solid_clustering(path_source=path_umap)
    path_topicwords = solids.solid_topicwords(path_source_topic_ids=path_clustering,
                                              path_source_documents=path_preprocessed)

    path_topics = solids.solid_topics(path_source_clustering=path_clustering,
                                      path_source_topicwords=path_topicwords)
    path_article_topic = solids.solid_article_topic(path_source_article=path_curated,
                                                    path_source_clustering=path_clustering,
                                                    path_source_embeddings=path_embeddings)
    path_frequencies = solids.solid_frequencies(path_source_article=path_curated,
                                                path_source_clustering=path_clustering)
    path_points = solids.solid_points(path_source=path_embeddings)


@dagster.pipeline(
    mode_defs=[mode_local, mode_dataproc],
    preset_defs=[preset_dev, preset_prod],
)
def pipeline_main():
    path_curated = composite_curated()
    composite_analytics(path_curated)


@dagster.pipeline(mode_defs=[mode_local, mode_dataproc], preset_defs=[preset_export])
def pipeline_export():
    path_target = solids.solid_export()


@dagster.schedule(
    cron_schedule='0 */3 * * *',
    pipeline_name='pipeline_main',
    mode='dataproc',
)
def schedule_main(context):
    return preset_prod.run_config


@dagster.repository
def repository_main():
    return [pipeline_export, pipeline_main, schedule_main]
