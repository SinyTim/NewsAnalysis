import logging
from pathlib import Path

from aggregator.raw.scraping.scraper import Scraper


def main():
    logging.basicConfig(level=logging.INFO)

    params = {
        'process_name': 'scraper',
        'path_destination': Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_data\raw'),
    }

    scraper = Scraper(**params)
    scraper.run()


if __name__ == '__main__':
    main()
