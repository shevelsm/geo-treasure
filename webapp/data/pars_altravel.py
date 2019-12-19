import requests
from bs4 import BeautifulSoup


def get_html(url):
    return requests.get(url).text


def get_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_pages():
    url = 'https://altertravel.ru/catalog/Краснодарский%20край'
    soup = get_soup(get_html(url))
    pages_list = soup.findAll('div', class_='in_catalog')['id']
    print(pages_list)


if __name__ == '__main__':
    get_pages()