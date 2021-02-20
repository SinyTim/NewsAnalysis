import dagster
import dagster_pyspark
from dagster.core.definitions.no_step_launcher import no_step_launcher

from aggregator.data_platform.orchestrator import resources
from aggregator.data_platform.orchestrator import solids


mode_local = dagster.ModeDefinition(
    name='local',
    resource_defs={
        'database': resources.postgres_database,
        'datalake': resources.datalake,
        'pyspark_step_launcher': no_step_launcher,
        'pyspark': dagster_pyspark.pyspark_resource.configured({'spark_conf': {
            'spark.jars.packages': 'io.delta:delta-core_2.12:0.8.0',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
            'spark.sql.catalog.spark_catalog': 'org.apache.spark.sql.delta.catalog.DeltaCatalog',
            'spark.default.parallelism': 2,
        }}),
    }
)


preset_local = dagster.PresetDefinition.from_files(
    name='local',
    config_files=[
        dagster.file_relative_path(__file__, '../../../../../configs/config_db.yaml'),
        dagster.file_relative_path(__file__, '../../../../../configs/config_lake.yaml'),
    ],
    mode='local',
)


@dagster.pipeline(mode_defs=[mode_local], preset_defs=[preset_local])
def pipeline_main():
    solids.solid_generator_tutby()
    # solid_generator_naviny()


@dagster.schedule(
    cron_schedule='*/3 * * * *',
    pipeline_name='pipeline_main',
    mode='local',
)
def schedule_main(context):
    return preset_local.run_config


@dagster.repository
def repository_main():
    return [pipeline_main, schedule_main]
