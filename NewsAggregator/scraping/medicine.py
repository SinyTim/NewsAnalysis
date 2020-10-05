import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path


def scrap(url_site: str, page_ids, verbose=True):
    """
    :param url_site:
        https://komzdrav-minsk.gov.by/news/{index}
        https://4gkb.by/news/{index}
    :return:
        pd.DataFrame(url, header, time, document)
    """

    data = []

    for page_id in page_ids:
        url_page = url_site.format(page_id)

        try:
            page = requests.get(url_page)
            content = page.content
            soup = BeautifulSoup(content, 'html.parser')

            header = soup.find_all('div', class_='page-header') \
                or soup.find_all('h2', class_='page-header')
            time = soup.find_all('div', class_='news__details__date')
            document = soup.find_all('div', class_='news__details__content')

            assert (len(header) == 1)
            assert (len(time) == 1)
            assert (len(document) == 1)

            header = header[0].get_text()
            time = time[0].get_text()
            document = document[0].get_text()

            data += [(url_page, header, time, document)]

        except AssertionError as error:
            if verbose:
                print(url_page, 'AssertionError')
        except Exception as exception:
            if verbose:
                print(url_page, 'Exception')

    data = pd.DataFrame(data, columns=['url', 'header', 'time', 'document'])

    return data


def transform(data: pd.DataFrame):

    data['header'] = data['header'].str.strip()

    data['time'] = data['time'].map(parse_russian_date)
    data['time'] = pd.to_datetime(data['time'], format='%d.%m.%Y')

    data['document'] = data['document'].str.strip()

    return data


months = {
    'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05',
    'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10',
    'ноября': '11', 'декабря': '12',
}


def parse_russian_date(date):
    """
    :param date: '%d %B(ru_RU) %Y'
    :return: '%d.%m.%Y'
    """
    day, month, year = date.split(' ')
    month = months[month]
    date = '.'.join((day, month, year))
    return date


if __name__ == '__main__':
    path_landing = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_datalake\landing\medicine')
    path_file = path_landing / Path('0.csv')

    path_landing.mkdir(exist_ok=True)

    urls = ['https://komzdrav-minsk.gov.by/news/{}/', 'https://4gkb.by/news/{}/']
    pages_ids = [range(1, 10), range(1, 10)]

    dfs = [scrap(url, page_ids) for url, page_ids in zip(urls, pages_ids)]
    dfs = [transform(df) for df in dfs]
    df = pd.concat(dfs, ignore_index=True)

    df.to_csv(path_file, index=False)
