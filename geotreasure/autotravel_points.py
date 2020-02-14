import logging
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from geotreasure.utils import save_point_to_db


def get_autotravel_points():
    """
    Parse and get intresting places from www.autotravel.ru and write them to the app db
    """
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

    try:
        response = ses.get(URL_SEARCH, params=params)
    except (requests.exceptions.ConnectionError, ValueError):
        logging.error("Connection error with {}".format(URL_BASE))
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    points_table = soup.find("table", class_="ttb tdc").find_all("tr")

    for point in points_table[1:]:
        href = point.find("a")["href"]
        url_point = f"{URL_BASE}{href}"
        data = point.find("td").text.split("\n")
        title_point = data[1].split("(")[0].strip()
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

        save_point_to_db(
            title_point, SOURCE, url_point, lat_point, long_point, info_point
        )
