import pandas as pd
from bs4 import BeautifulSoup

from aggregator.data_platform.structured.structured_html_etl import StructuredHtmlEtl


class StructuredEtlMedicine(StructuredHtmlEtl):

    def __init__(self, **kwargs):
        parse_return_type = 'header string, time string, document string'
        super().__init__(parse_return_type=parse_return_type, **kwargs)

    def get_parser(self):

        class Parser:
            def __call__(self, html):
                return self.parse_html(html)

            def parse_html(self, html):

                soup = BeautifulSoup(html, 'html.parser')

                header = soup.find_all('div', class_='page-header') or soup.find_all('h2', class_='page-header')
                time = soup.find_all('div', class_='news__details__date')
                document = soup.find_all('div', class_='news__details__content')

                if (len(header) != 1) or (len(time) != 1) or (len(document) != 1):
                    error = f'invalid tags number: header - {len(header)}, time - {len(time)}, document - {len(document)}'
                    return None, None, None, error

                header = header[0].get_text()
                time = time[0].get_text()
                document = document[0].get_text()

                header, time, document = self.process(header, time, document)

                return header, time, document, None

            def process(self, header, time, document):

                header = header.strip()
                document = document.strip()
                time = self.parse_russian_date(time)

                return header, time, document

            def parse_russian_date(self, date):
                """
                :param date: '%d %B(ru_RU) %Y'
                :return: '%d.%m.%Y'
                """

                day, month, year = date.split(' ')
                month = self.months[month]
                date = '.'.join((day, month, year))

                date = pd.to_datetime(date, format='%d.%m.%Y')
                date = date.strftime('%Y-%m-%d %H:%M')

                return date

            months = {
                'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05',
                'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10',
                'ноября': '11', 'декабря': '12',
            }

        return Parser()
