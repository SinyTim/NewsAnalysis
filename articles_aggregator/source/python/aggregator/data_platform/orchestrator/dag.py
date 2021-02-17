import dagster
import dagster_pyspark
from dagster.core.definitions.no_step_launcher import no_step_launcher


mode_local = dagster.ModeDefinition(
    name='local',
    resource_defs={
        'pyspark_step_launcher': no_step_launcher,
        'pyspark': dagster_pyspark.pyspark_resource
    }
)


@dagster.solid
def get_name(context, default: str) -> str:
    return default or 'dagster'


@dagster.solid(required_resource_keys={'pyspark', 'pyspark_step_launcher'})
def hello(context, name: str) -> None:
    spark = context.resources.pyspark.spark_session
    context.log.info(f'Hello, {name}!')
    x = range(1000)
    x = spark.sparkContext.parallelize(x)
    context.log.info(str(x.take(5)))
    return x


@dagster.pipeline(mode_defs=[mode_local])
def hello_pipeline():
    name = get_name()
    hello(name)


@dagster.schedule(
    cron_schedule='*/1 * * * *',
    pipeline_name='hello_pipeline',
)
def hello_schedule(date):
    return {
        'solids': {
            'get_name': {'inputs': {'default': {'value': str(date)}}}
        }
    }


@dagster.repository
def hello_repository():
    return [hello_pipeline, hello_schedule]


if __name__ == "__main__":

    run_config = {
        'solids': {
            'get_name': {'inputs': {'default': {'value': 'World'}}}
        }
    }

    dagster.execute_pipeline(hello_pipeline, run_config=run_config)

# dagster-daemon run
# dagit -f dag.py
