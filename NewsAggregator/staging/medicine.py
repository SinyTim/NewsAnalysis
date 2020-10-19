from bs4 import BeautifulSoup
import pandas as pd

from staging import utils


def extract(html):

    soup = BeautifulSoup(html, 'html.parser')

    header = soup.find_all('div', class_='page-header') or soup.find_all('h2', class_='page-header')
    time = soup.find_all('div', class_='news__details__date')
    document = soup.find_all('div', class_='news__details__content')

    if ((len(header) != 1)
            or (len(time) != 1)
            or (len(document) != 1)):
        return None, f'invalid tags number: header - {len(header)}, time - {len(time)}, document - {len(document)}'

    header = header[0].get_text()
    time = time[0].get_text()
    document = document[0].get_text()

    return header, time, document


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


def main():
    process_name = 'staging_medicine'
    source = 'medicine_0'
    columns = ['header', 'time', 'document']

    utils.run(process_name, source, extract, columns, transform)

    process_name = 'staging_medicine'
    source = 'medicine_1'
    columns = ['header', 'time', 'document']

    utils.run(process_name, source, extract, columns, transform)


if __name__ == '__main__':
    main()
