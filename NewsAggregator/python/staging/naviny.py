from bs4 import BeautifulSoup
import pandas as pd
from staging.staging_etl import StagingHtmlEtl


class StagingEtlNaviny(StagingHtmlEtl):

    def __init__(self, **kwargs):
        columns = ['header', 'time', 'label', 'n_views', 'document', 'tags']
        super().__init__(columns=columns, **kwargs)

    def parse_html(self, html):

        soup = BeautifulSoup(html, 'html.parser')

        header = soup.find_all('h1')
        if len(header) != 1:
            return f'invalid tags number: header - {len(header)}'
        header = header[0].get_text()
        header = header.strip()

        info = soup.find_all('div', class_='article-info')
        if len(info) != 1:
            return f'invalid tags number: article-info - {len(info)}'

        info = info[0].find_all('div', class_='pull-left')
        if len(info) != 2:
            return f'invalid tags number: pull-left - {len(info)}'

        time = info[0].time.get_text()
        time = pd.to_datetime(time, format='%d.%m.%Y / %H:%M')
        time = time.strftime('%Y-%m-%d %H:%M')

        label = info[0].a.get_text() if info[0].a else None

        n_views = info[1].span.get_text()
        n_views = int(n_views.split(' ')[-1])

        document = soup.find_all(lambda tag: tag.has_attr('data-io-article-url'))
        if len(document) != 1:
            return f'invalid tags number: document - {len(document)}'
        document = document[0].get_text()
        document = document.strip()

        tags = soup.find_all('div', class_='af-tags')
        if len(tags) != 1:
            return f'invalid tags number: tags - {len(tags)}'
        tags = tags[0].findChildren('a', recursive=False)
        tags = [tag.get_text() for tag in tags]

        return header, time, label, n_views, document, tags
