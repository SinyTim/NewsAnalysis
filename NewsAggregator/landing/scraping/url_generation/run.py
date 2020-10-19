from landing.scraping.url_generation.generator_int import UrlGeneratorWithIntState


def main():

    params = [
        {
            'source': 'tutby',
            'process_name': 'url_generator_int',
            'url_template': 'https://news.tut.by/{}.html',
            'default_start_state': '704600',
            'max_n_fails': 10,
        },
        {
            'source': 'medicine_0',
            'process_name': 'url_generator_int',
            'url_template': 'https://komzdrav-minsk.gov.by/news/{}',
            'default_start_state': '345',
            'max_n_fails': 5,
        },
        {
            'source': 'medicine_1',
            'process_name': 'url_generator_int',
            'url_template': 'https://4gkb.by/news/{}',
            'default_start_state': '130',
            'max_n_fails': 5,
        }
    ]

    for param in params:
        generator = UrlGeneratorWithIntState(**param)
        generator.run()


if __name__ == '__main__':
    main()
