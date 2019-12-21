import requests
import os
from bs4 import BeautifulSoup
from webapp.app import db, app
from webapp.model import Point


def get_html(url):
    return requests.get(url).text


def get_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_pages_id(region_url):
    soup = get_soup(get_html(region_url))
    pages_list = soup.findAll('div', class_='in_catalog')
    id_list = []
    for page in pages_list:
        id_list.append(page['id'][2:])
    return id_list


def get_page_info(id):
    url = 'https://altertravel.ru/view.php?id=' + id
    soup = get_soup(get_html(url))
    title = soup.find('h1', class_='view').text
    source = 'altertravel'
    info = soup.find('div', class_='col-sm-4').find('p').text.strip()
    info = info.split('\n')[0]
    coords = soup.find('div', class_='points').find('span').text
    coords_list = coords.replace(',', '').split()
    lat = float(coords_list[0])
    long = float(coords_list[1])
    return title, source, url, lat, long, info


def save_info_to_bd(title, source, url, lat, long, info):
    point_exists = Point.query.filter(Point.url == url).count()
    if not point_exists:
        point = Point(title=title, 
                      source=source,
                      url=url,
                      lat=lat,
                      long=long,
                      info=info)
        db.session.add(point)
        db.session.commit()


if __name__ == '__main__':
    region_url = 'https://altertravel.ru/catalog/Краснодарский%20край'
    pages_id = get_pages_id(region_url)
    with app.app_context():
        for page_id in pages_id:
            save_info_to_bd(*get_page_info(page_id))