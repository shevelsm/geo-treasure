import logging
import re
from os import environ

import requests
from bs4 import BeautifulSoup

from webapp.utils import save_point_to_db


def get_geocaching_points():
    """
    Parse and get intresting places from www.geocaching.su and write them to the app db
    """
    zones = {
        "Адыгея респ.": {"country": 10, "area": 1},
        "Краснодарский край": {"country": 10, "area": 23},
    }

    URL = "https://geocaching.su/"
    SOURCE = "geocaching"
    POINT_PAGE = "101"
    SEARCH_PAGE = "102"
    MIN_RATING = 4

    form_login = {
        "Log_In": "Log_In",
        "email": environ["GEOCACHING_LOGIN"],
        "passwd": environ["GEOCACHING_PWD"],
        "longterm": 1,
    }

    try:
        ses = requests.Session()
        ses.post(URL, data=form_login)
    except (requests.exceptions.ConnectionError, ValueError):
        logging.error("Connection error with {}".format(URL))
        return False

    for zone_data in zones.values():
        form_data = {
            "search_type": 10,
            "condition": 1111111,
            "country": zone_data["country"],
            "area": zone_data["area"],
            "rating": MIN_RATING,
        }
        params = {"pn": SEARCH_PAGE}
        response = ses.post(URL, data=form_data, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        points_table = soup.find("table", class_="pages").find_all(
            "tr", {"valign": "top"}
        )

        for point in points_table:
            id_point = point.find("input")["value"]
            title_point = point.find("a").text.strip()
            logging.debug(f" Point id: {id_point}")
            logging.debug(f" Point title: {title_point}")

            params = {
                "pn": POINT_PAGE,
                "cid": id_point,
            }
            response = ses.get(URL, params=params)
            url_point = response.url
            soup = BeautifulSoup(response.text, "html.parser")

            coords = soup.find("th", {"id": "cache_coords"})
            coords = re.sub("[NSEW°']", "", coords.text).strip().split()
            lat_point = float(coords[0]) + float(coords[1]) / 60
            long_point = float(coords[2]) + float(coords[3]) / 60
            logging.debug(f"Coords: lat={lat_point} long={long_point}")

            info_text = soup.find("div", class_="cdata").find_all("p")
            if info_text:
                info_point = ""
                for paragraph in info_text:
                    info_point += paragraph.text.strip()
            else:
                info_point = "Информация отсутствует"

            save_point_to_db(
                title_point, SOURCE, url_point, lat_point, long_point, info_point
            )
