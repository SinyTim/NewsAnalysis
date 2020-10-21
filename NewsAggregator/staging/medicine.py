from bs4 import BeautifulSoup
import pandas as pd

from staging.staging_etl import StagingHtmlEtl


class StagingEtlMedicine(StagingHtmlEtl):

    def __init__(self, **kwargs):

        columns = ['header', 'time', 'document']

        super().__init__(columns=columns, **kwargs)

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        header = soup.find_all('div', class_='page-header') or soup.find_all('h2', class_='page-header')
        time = soup.find_all('div', class_='news__details__date')
        document = soup.find_all('div', class_='news__details__content')

        if ((len(header) != 1)
                or (len(time) != 1)
                or (len(document) != 1)):
            return f'invalid tags number: header - {len(header)}, time - {len(time)}, document - {len(document)}'

        header = header[0].get_text()
        time = time[0].get_text()
        document = document[0].get_text()

        header, time, document = self._process(header, time, document)

        return header, time, document

    def _process(self, header, time, document):

        header = header.strip()
        document = document.strip()

        time = self._parse_russian_date(time)
        time = pd.to_datetime(time, format='%d.%m.%Y')

        return header, time, document

    def _parse_russian_date(self, date):
        """
        :param date: '%d %B(ru_RU) %Y'
        :return: '%d.%m.%Y'
        """

        day, month, year = date.split(' ')
        month = StagingEtlMedicine.months[month]
        date = '.'.join((day, month, year))
        return date

    months = {
        'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05',
        'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10',
        'ноября': '11', 'декабря': '12',
    }
