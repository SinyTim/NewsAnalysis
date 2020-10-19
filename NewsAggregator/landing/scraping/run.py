from pathlib import Path

from landing.scraping.scraper import Scraper


def main():

    params = {
        'process_name': 'scraper',
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\landing'),
    }

    scraper = Scraper(**params)
    scraper.run()


if __name__ == '__main__':
    main()
