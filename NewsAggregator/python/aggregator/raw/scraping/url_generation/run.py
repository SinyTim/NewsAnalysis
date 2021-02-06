import logging

from aggregator.raw.scraping.url_generation.generator_date import UrlGeneratorWithDateState
from aggregator.raw.scraping.url_generation.generator_int import UrlGeneratorWithIntState


def main():
    logging.basicConfig(level=logging.INFO)

    params = [
        {
            'source': 'komzdrav',
            'process_name': 'url_generator_int',
            'url_template': 'https://komzdrav-minsk.gov.by/news/{}',
            'default_start_state': '1',
            'max_n_fails': 5,
        },
        {
            'source': '4gkb',
            'process_name': 'url_generator_int',
            'url_template': 'https://4gkb.by/news/{}',
            'default_start_state': '1',
            'max_n_fails': 35,
        },
        {
            'source': 'tutby',
            'process_name': 'url_generator_int',
            'url_template': 'https://news.tut.by/{}.html',
            'default_start_state': '717000',
            'max_n_fails': 10,
        },
    ]

    for param in params:
        generator = UrlGeneratorWithIntState(**param)
        generator.run()

    params = {
        'source': 'naviny',
        'process_name': 'url_generator_date',
        'url_template': 'https://naviny.media/day/{}',
        'default_start_state': '2021/01/28',
    }

    generator = UrlGeneratorWithDateState(**params)
    generator.run()


if __name__ == '__main__':
    main()
