import pandas as pd
from bs4 import BeautifulSoup

from aggregator.data_platform.structured.structured_html_etl import StructuredHtmlEtl


class StructuredEtlTutby(StructuredHtmlEtl):

    def __init__(self, **kwargs):
        parse_return_type = 'label string, header string, n_comments int, time string, document string, tags array<string>'
        super().__init__(parse_return_type=parse_return_type, **kwargs)

    def get_parser(self):
        return parse_html


def parse_html(html):

    soup = BeautifulSoup(html, 'html.parser')

    label = soup.find_all('a', attrs={'itemprop': 'articleSection'})
    header = soup.find_all('h1', attrs={'itemprop': 'headline'})
    n_comments = soup.find_all('span', attrs={'itemprop': 'commentCount'})
    time = soup.find_all('time', attrs={'itemprop': 'datePublished'})
    document = soup.find_all('div', attrs={'itemprop': 'articleBody'})
    tags = soup.find_all('li', class_='tag-taxonomy-topic')

    if ((len(label) != 1)
            or (len(header) != 1)
            or (len(n_comments) != 1 and len(n_comments) != 0)
            or (len(time) != 1)
            or (len(document) != 1)
            or (len(tags) != 1 and len(tags) != 0)):
        error = f'invalid tags number: label - {len(label)}, header - {len(header)}, n_comments - {len(n_comments)}, time - {len(time)}, document - {len(document)}, tags - {len(tags)}'
        return None, None, None, None, None, None, error

    label = label[0].get_text()
    header = header[0].get_text()
    n_comments = n_comments[0].get_text() if n_comments else None

    time = time[0]['datetime']
    time = pd.to_datetime(time)
    time = time.strftime('%Y-%m-%d %H:%M')

    document = document[0].get_text()

    tags = tags[0].findChildren('a', recursive=False) if tags else []
    tags = [tag.get_text() for tag in tags]

    header = header.strip()
    document = document.strip()

    return label, header, n_comments, time, document, tags, None
