from landing.scraping.url_generation.generator_int import UrlGeneratorWithIntState


def main():

    params = [
        {
            'source': 'medicine_0',
            'process_name': 'url_generator_int',
            'url_template': 'https://komzdrav-minsk.gov.by/news/{}',
            'default_start_state': '1',
            'max_n_fails': 5,
        },
        {
            'source': 'medicine_1',
            'process_name': 'url_generator_int',
            'url_template': 'https://4gkb.by/news/{}',
            'default_start_state': '1',
            'max_n_fails': 35,
        },
        {
            'source': 'tutby',
            'process_name': 'url_generator_int',
            'url_template': 'https://news.tut.by/{}.html',
            'default_start_state': '704500',
            'max_n_fails': 10,
        },
    ]

    for param in params:
        generator = UrlGeneratorWithIntState(**param)
        generator.run()


if __name__ == '__main__':
    main()
