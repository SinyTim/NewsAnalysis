from landing.scraping.url_generation.run import main as main_generation
from landing.scraping.run import main as main_scraping
from staging.run import main as main_staging
from dw.run import main as main_dw
from text_preprocessing.run import main as main_preprocessing
from embedding.run import main as main_embedding


def main():
    main_generation()
    main_scraping()
    main_staging()
    main_dw()
    main_preprocessing()
    main_embedding()


if __name__ == '__main__':
    main()
