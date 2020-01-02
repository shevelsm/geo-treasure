import logging
import re
from os import environ

import requests
from bs4 import BeautifulSoup

from webapp.model import db, Point


logging.basicConfig(level=logging.DEBUG, filename="autotravel_parsing.log")


def save_to_db(
    title_point, source_point, url_point, lat_point, long_point, info_point
):
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
    URL_DATA = "https://autotravel.ru/test.php?area%5B%5D=28&area%5B%5D=69&typex%5B%5D=000&typex%5B%5D=029&typex%5B%5D=003&typex%5B%5D=011&typex%5B%5D=009&typex%5B%5D=002&typex%5B%5D=018&typex%5B%5D=006&typex%5B%5D=015&typex%5B%5D=053&typex%5B%5D=007&typex%5B%5D=005&typex%5B%5D=040&typex%5B%5D=050&typex%5B%5D=051&typex%5B%5D=024&typex%5B%5D=028&typex%5B%5D=012&typex%5B%5D=004&typex%5B%5D=032&typex%5B%5D=039&typex%5B%5D=057&typex%5B%5D=010&typex%5B%5D=042&typex%5B%5D=054&typex%5B%5D=056&typex%5B%5D=016&typex%5B%5D=033&typex%5B%5D=043&typex%5B%5D=055&typex%5B%5D=038&typex%5B%5D=052&typex%5B%5D=023&typex%5B%5D=019&typex%5B%5D=034&typex%5B%5D=027&typex%5B%5D=025&typex%5B%5D=059&typex%5B%5D=008&typex%5B%5D=030&typex%5B%5D=026&typex%5B%5D=001&typex%5B%5D=036&typex%5B%5D=013&typex%5B%5D=031&typex%5B%5D=047&typex%5B%5D=048&typex%5B%5D=014&typex%5B%5D=062&typex%5B%5D=058&typex%5B%5D=049&typex%5B%5D=022&typex%5B%5D=060&typex%5B%5D=020&typex%5B%5D=021&typex%5B%5D=061&mrate=0.01&adiff=0&tid=0&helptid=&search=&mark=1&ksubmit=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8"
    SOURCE = "autotravel"
    AREAS = {
        "Краснодарский край": 28,
        "Республика Адыгея": 69,
    }

    ses = requests.Session()
    response = ses.get(URL_DATA)
    soup = BeautifulSoup(response.text, "html.parser")
    points_table = soup.find("table", class_="ttb tdc").find_all("tr")

    for point in points_table[1:]:
        href = point.find("a")["href"]
        url_point = f"{URL_BASE}{href}"
        data = point.find("td").text.split("\n")
        title_point = data[1].split("(")[0]
        logging.debug(f"New point title: {title_point}")
        coords = re.sub("[N,E]","",data[2]).split()
        try:
            lat_point = float(coords[0]) + float(coords[1]) / 60
            long_point = float(coords[2]) + float(coords[3]) / 60
            logging.debug(f"Coords: lan={lat_point} long={long_point}")
        except ValueError:
            continue

        response = ses.get(url_point)
        soup = BeautifulSoup(response.text, "html.parser")
        info_point = soup.find("p").text
        logging.debug(f"Point info:\n{info_point}")
        
        save_to_db(
            title_point, SOURCE, url_point, lat_point, long_point, info_point
        )