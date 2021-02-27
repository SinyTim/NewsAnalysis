from pathlib import Path

import dagster

from aggregator.data_platform.utils.postgres_connection import PostgresConnection


@dagster.resource(
    config_schema={
        'host': str,
        'port': int,
        'db_name': str,
        'user_name': str,
        'user_password': str,
    },
)
def postgres_database(context):
    return PostgresConnection(**context.resource_config)


@dagster.resource(config_schema={'path': str})
def datalake(context):
    return Path(context.resource_config['path'])
