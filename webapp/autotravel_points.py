import logging
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from webapp.model import db, Point


def save_to_db(title_point, source_point, url_point, lat_point, long_point, info_point):
    point_exist = Point.query.filter(Point.url == url_point).count()
    logging.debug(f"count this point {point_exist}")
    if not point_exist:
        new_point = Point(
            title=title_point,
            source=source_point,
            url=url_point,
            lat=lat_point,
            long=long_point,
            info=info_point,
        )
        db.session.add(new_point)
        db.session.commit()


def get_autotravel_points():
    URL_BASE = "https://autotravel.ru"
    SEARCH_PAGE = "test.php"
    URL_SEARCH = urljoin(URL_BASE, SEARCH_PAGE)
    SOURCE = "autotravel"
    AREAS = {
        "Краснодарский край": 28,
        "Республика Адыгея": 69,
    }
    NUMBER_OF_POINTS_TYPES_IN_SEARCH = 63
    POINTS_TYPES = [f"{n:03}" for n in range(NUMBER_OF_POINTS_TYPES_IN_SEARCH)]

    ses = requests.Session()
    params = {
        "area[]": AREAS.values(),
        "typex[]": POINTS_TYPES,
        "mrate": 0.01,
        "diff": 0,
        "tid": 0,
        "helptid": 0,
        "mark": 1,
        "ksubmit": "Найти",
    }
    response = ses.get(URL_SEARCH, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    points_table = soup.find("table", class_="ttb tdc").find_all("tr")

    for point in points_table[1:]:
        href = point.find("a")["href"]
        url_point = f"{URL_BASE}{href}"
        data = point.find("td").text.split("\n")
        title_point = data[1].split("(")[0]
        logging.debug(f"New point title: {title_point}")
        coords = re.sub("[N,E]", "", data[2]).split()
        try:
            lat_point = float(coords[0]) + float(coords[1]) / 60
            long_point = float(coords[2]) + float(coords[3]) / 60
            logging.debug(f"Coords: lat={lat_point} long={long_point}")
        except ValueError:
            continue

        response = ses.get(url_point)
        soup = BeautifulSoup(response.text, "html.parser")
        info_point = soup.find("p").text
        logging.debug(f"Point info:\n{info_point}")

        save_to_db(title_point, SOURCE, url_point, lat_point, long_point, info_point)
