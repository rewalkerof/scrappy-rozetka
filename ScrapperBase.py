import requests
from bs4 import BeautifulSoup


class ScrapperBase:
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