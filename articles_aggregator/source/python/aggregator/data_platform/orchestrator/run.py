import dagster

from aggregator.data_platform.orchestrator import repository
from aggregator.data_platform.orchestrator import solids


if __name__ == '__main__':

    repository.preset_local.run_config.pop('solids')

    dagster.execute_solid(
        solids.solid_structured_komzdrav,
        mode_def=repository.mode_local,
        input_values={
            'path_source': 'raw/html/komzdrav.delta',
            'path_target': 'structured/komzdrav.delta',
        },
        run_config=repository.preset_local.run_config
    )
