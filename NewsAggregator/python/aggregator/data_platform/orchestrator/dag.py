import dagster


@dagster.solid
def get_name(context, default: str) -> str:
    return default or 'dagster'


@dagster.solid
def hello(context, name: str) -> None:
    context.log.info(f'Hello, {name}!')


@dagster.pipeline
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
