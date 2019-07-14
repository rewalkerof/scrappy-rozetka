import re

import requests
from bs4 import BeautifulSoup


class ScrapperMixin:
    @staticmethod
    def get_html(url):
        try:
            return requests.get(url, timeout=10).text
        except requests.exceptions.ConnectionError:
            print('URL is unavailable')
            exit()

    @staticmethod
    def get_soup(html, parser='html.parser', tags_to_delete=None):
        if tags_to_delete is None:
            tags_to_delete = ()
        soup = BeautifulSoup(html, parser)
        for tag in tags_to_delete:
            for tg in soup.find_all(tag):
                tg.replaceWith('')
        return soup

    @staticmethod
    def repeat_until_done(func):
        def wrapped(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except AttributeError:
                    print('Error. Trying to do it again.')

        return wrapped


class RozetkaScrapper:
    BASE_URL = 'https://rozetka.com.ua/notebooks/c80004/filter/'

    @ScrapperMixin.repeat_until_done
    def get_count_pages(self, url):
        soup = ScrapperMixin.get_soup(ScrapperMixin.get_html(url), tags_to_delete=('script',))
        pages_anc = \
        soup.find('nav', class_='paginator-catalog pos-fix').find_all('a', class_='blacklink paginator-catalog-l-link')[
            -1].get('href')
        total = pages_anc.split('/')[-2].split('=')[1] or re.search(r'1\d{2}', pages_anc)[0]
        return int(total)

    @ScrapperMixin.repeat_until_done
    def get_page_data(self, url):
        dct_data = {}
        soup = ScrapperMixin.get_soup(ScrapperMixin.get_html(url), tags_to_delete=('script',))
        product_catalog = soup.find('div', class_='g-i-tile-l g-i-tile-catalog-hover-left-side clearfix').find_all(
            'div', class_='g-i-tile g-i-tile-catalog')
        for item, product in enumerate(product_catalog, 1):
            product = {'title': product.find('div', class_='g-i-tile-i-title clearfix').find('a').next.strip(),
                       'url': product.find('a').get('href')}
            dct_data[item] = product
        return dct_data

    def __init__(self):
        self.url = RozetkaScrapper.BASE_URL
        total_pages = self.get_count_pages(self.url)

        for page in range(1, total_pages + 1):
            url = f'{self.url}page={int(page)}/'
            dct_data = self.get_page_data(url)
            print(f'\n\t\t\t\tPage: {page} ', end='\n\n')

            for item, value in dct_data.items():
                print('\n{}. {} \n\turl: {}\n\tprice: None'.format(item, value['title'], value['url']))


if __name__ == '__main__':
    RozetkaScrapper()
