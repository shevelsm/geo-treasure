import logging

import requests
from bs4 import BeautifulSoup

from webapp.model import db, Point
from webapp.utils import save_point_to_db


def get_html(url):
    return requests.get(url).text


def get_html_params(url, params):
    return requests.post(url=url, params=params)


def get_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_pages_id(region_name):
    url = 'https://altertravel.ru/catalog_sub.php'
    page_number = 0
    id_list = []
    while True:
        params = {'p': page_number, 'tag': region_name}
        soup = get_soup(get_html_params(url, params).text)
        # search for end
        if soup.find('div', class_='roww'):
            logging.debug(f'complete parsing {region_name} ids')
            break
        pages_list = soup.findAll('div', class_='info_title')
        for page in pages_list:
            id_list.append(page.find('a')['href'][13:])
        page_number += 1
    return id_list


def get_page_info(page_id):
    url = f'https://altertravel.ru/view.php?id={page_id}'
    soup = get_soup(get_html(url))
    title = soup.find('h1', class_='view').text
    logging.debug(f'New point title: {title}')
    source = 'altertravel'
    try:
        info = soup.find('div', class_='col-sm-4').find('p').text.strip()
        info = info.split('\n')[0]
    except AttributeError:
        info = ''
    coords = soup.find('div', class_='points').find('span').text
    coords_list = coords.replace(',', '').split()
    lat = float(coords_list[0])
    long = float(coords_list[1])
    logging.debug(f'Coords: lat={lat} long={long}')
    return title, source, url, lat, long, info


def get_altravel_points():
    region_names = ['Краснодарский край',
                    'Республика Адыгея',
    ]
    pages_id = []
    for region in region_names:
        pages_id += get_pages_id(region)
    for page_id in pages_id:
        save_point_to_db(*get_page_info(page_id))
