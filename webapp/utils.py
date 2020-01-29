import json
import logging
import os

from folium import Icon, Popup, Html
from branca.element import Element

from webapp.model import db, Point, ClusterPoint


def save_point_to_db(title, source, url, lat, long, info):
    url_exists = Point.query.filter(Point.url == url).count()
    title_exists = Point.query.filter(Point.title == title).count()
    logging.debug(f"count this point {url_exists or title_exists}")
    if not (url_exists or title_exists):
        point = Point(
            title=title, source=source, url=url, lat=lat, long=long, info=info,
        )
        db.session.add(point)
        db.session.commit()


def create_popup_and_icon(query_list):
    # generate icon
    number_of_points = len(query_list)

    if number_of_points < 5:
        icon_color = "blue"
    elif number_of_points < 7:
        icon_color = "pink"
    elif number_of_points < 14:
        icon_color = "purple"
    elif number_of_points < 36:
        icon_color = "red"
    else:
        icon_color = "darkred"

    # generate popup
    sources = [row[4] for row in query_list]
    alter, auto, geo = (
        sources.count("altertravel"),
        sources.count("autotravel"),
        sources.count("geocaching"),
    )

    text = Html(
        f"Количество интересных мест в точке:<br>"
        f"c сайта altertravel - {alter} шт.<br>" 
        f"с сайта autotravel - {auto} шт.<br>" 
        f"с сайта geocaching - {geo} шт.",
        script=True,
    )

    return Popup(html=text, max_width=400), Icon(color=icon_color, icon="gift")


def add_on_click_handler_to_marker(folium_map, marker, cluster_id, host_url):
    my_js = """
            {0}.on('click', function(e) {{
                parent.postMessage({1}, "{2}");
            }});
            """.format(
        marker.get_name(), cluster_id, host_url
    )
    e = Element(my_js)
    html = folium_map.get_root()
    html.script.get_root().render()
    html.script._children[e.get_name()] = e


def markers_generator():
    """ range - searching radius for places """
    path_to_file = os.path.join("webapp", "data", "ready50dots.json")
    with open(path_to_file, "r", encoding="utf-8") as file:
        markers_data = json.loads(file.read())
    return markers_data
