import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path


def scrap(url_site: str, page_ids, verbose=True):
    """
    :param url_site:
        'https://news.tut.by/{index}.html'
    :return:
        pd.DataFrame(url, label, header, n_comments, time, document, tags)
    """

    data = []

    for page_id in page_ids:
        url_page = url_site.format(page_id)

        try:
            response = requests.get(url_page)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')

            label = soup.find_all('a', attrs={'itemprop': 'articleSection'})
            header = soup.find_all('h1', attrs={'itemprop': 'headline'})
            n_comments = soup.find_all('span', attrs={'itemprop': 'commentCount'})
            time = soup.find_all('time', attrs={'itemprop': 'datePublished'})
            document = soup.find_all('div', attrs={'itemprop': 'articleBody'})
            tags = soup.find_all('li', class_='tag-taxonomy-topic')

            assert (len(label) == 1)
            assert (len(header) == 1)
            assert (len(n_comments) == 1 or len(n_comments) == 0)
            assert (len(time) == 1)
            assert (len(document) == 1)
            assert (len(tags) == 1 or len(tags) == 0)

            label = label[0].get_text()
            header = header[0].get_text()
            n_comments = n_comments[0].get_text() if n_comments else None
            time = time[0]['datetime']
            document = document[0].get_text()

            tags = tags[0].findChildren('a', recursive=False) if tags else []
            tags = [tag.get_text() for tag in tags]

            data += [(url_page, label, header, n_comments, time, document, tags)]

        except AssertionError as error:
            if verbose:
                print(url_page, 'AssertionError', error)
        except Exception as exception:
            if verbose:
                print(url_page, 'Exception', exception)

    data = pd.DataFrame(data, columns=['url', 'label', 'header', 'n_comments', 'time', 'document', 'tags'])

    return data


if __name__ == '__main__':
    path_landing = Path(r'C:\Users\Tim\Documents\GitHub\NewsAnalysis\data\_datalake\landing\tutby')
    path_file = path_landing / Path('0.csv')

    path_landing.mkdir(exist_ok=True)

    url = 'https://news.tut.by/{}.html'

    page_ids = range(1, 1 + 5)
    df = scrap(url, page_ids)
    df.to_csv(path_file, index=False)

    page_ids = range(702462 - 5, 702462)
    df = scrap(url, page_ids)
    df.to_csv(path_landing / Path('1.csv'), index=False)
