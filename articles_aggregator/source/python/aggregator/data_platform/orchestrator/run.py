import dagster

from aggregator.data_platform.orchestrator import repository
from aggregator.data_platform.orchestrator import solids


def main():

    # repository.preset_dev.run_config.pop('solids')
    #
    # dagster.execute_solid(
    #     solids.solid_points,
    #     mode_def=repository.mode_local,
    #     input_values={
    #         'path_source': 'analytics/embedding.delta',
    #         'path_target': 'consumer/points.parquet',
    #     },
    #     run_config=repository.preset_dev.run_config
    # )

    # repository.preset_dev.run_config['solids'] = {'solid_topicwords': {'config': {'path_idf': 'models/idf/idf.csv'}}}
    #
    # dagster.execute_solid(
    #     solids.solid_topicwords,
    #     mode_def=repository.mode_local,
    #     input_values={
    #         'path_source_topic_ids': 'analytics/clustering.delta',
    #         'path_source_documents': 'analytics/preprocessed.delta',
    #         'path_target': 'analytics/topicwords.delta',
    #     },
    #     run_config=repository.preset_dev.run_config
    # )

    # x = [
    #     'solid_curated_4gkb', 'solid_curated_komzdrav', 'solid_generator_4gkb',
    #     'solid_generator_komzdrav', 'solid_scraper_4gkb', 'solid_scraper_komzdrav',
    #     'solid_structured_4gkb', 'solid_structured_komzdrav'
    # ]
    #
    # for c in x:
    #     if c in repository.preset_dev.run_config['solids']:
    #         repository.preset_dev.run_config['solids'].pop(c)

    dagster.execute_pipeline(
        repository.pipeline_main,
        preset='dev',
    )


if __name__ == '__main__':
    main()
