import dagster

from aggregator.data_platform.orchestrator import repository
from aggregator.data_platform.orchestrator import solids


if __name__ == '__main__':

    repository.preset_local.run_config['solids'].pop('solid_generator_naviny')
    repository.preset_local.run_config['solids'].pop('solid_generator_4gkb')
    repository.preset_local.run_config['solids'].pop('solid_generator_komzdrav')
    repository.preset_local.run_config['solids'].pop('solid_generator_tutby')

    dagster.execute_solid(
        solids.solid_scraper_tutby,
        mode_def=repository.mode_local,
        input_values={
            'path_source': 'raw/urls/tutby.delta',
        },
        run_config=repository.preset_local.run_config
    )
