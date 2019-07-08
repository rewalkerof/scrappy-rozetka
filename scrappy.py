import requests
import re
from bs4 import BeautifulSoup

BASE_URL = 'https://rozetka.com.ua/notebooks/c80004/filter/'


def get_html(url=BASE_URL):
    req = requests.get(url, timeout=5)
    return req.text


def get_soup(html, parser='html.parser', tags_to_delete=None):
    if tags_to_delete is None:
        tags_to_delete = ()
    soup = BeautifulSoup(html, parser)
    for tag in tags_to_delete:
        for tg in soup.find_all(tag):
            tg.replaceWith('')
    return soup


def get_count_pages(url=BASE_URL):
    while True:
        try:
            soup = get_soup(get_html(url), tags_to_delete=('script',))
            pages_anc = soup.find('nav', class_='paginator-catalog pos-fix').find_all('a', class_='blacklink paginator-catalog-l-link')[-1].get('href')
            break
        except AttributeError:
            print('Error. Trying to connect again.')
    total = pages_anc.split('/')[-2].split('=')[1] or re.search(r'1\d{2}', pages_anc)[0]
    return int(total)


def get_page_data(url):
    while True:
        try:
            dct_data = {}
            soup = get_soup(get_html(url), tags_to_delete=('script',))
            product_catalog = soup.find('div', class_='g-i-tile-l g-i-tile-catalog-hover-left-side clearfix').find_all(
                'div', class_='g-i-tile g-i-tile-catalog')
            for item, product in enumerate(product_catalog, 1):
                dct_data.setdefault(item, {})['title'] = product.find('div', class_='g-i-tile-i-title clearfix').find(
                    'a').next.strip()
                dct_data.setdefault(item, {})['url'] = product.find('a').get('href')
            break
        except AttributeError:
            print('Error. Trying to connect again.')
    return dct_data


def main():
    total_pages = get_count_pages()

    for page in range(1, total_pages+1):
        url = f'{BASE_URL}page={int(page)}/'
        try:
            dct_data = get_page_data(url)
        except requests.exceptions.ConnectionError:
            print('Rozetka is unavailable')
            return

        print(f'\n\t\t\t\tPage: {page} ', end='\n\n')

        for item, value in dct_data.items():
            print(''.join('\n{}. {} \n\turl: {}\n\tprice: None'.format(item, value['title'], value['url'])))


if __name__ == '__main__':
    main()
