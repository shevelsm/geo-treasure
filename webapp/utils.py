import json
import logging
import os

from branca.element import Element
from folium import Icon, Popup, Html
import matplotlib.pyplot as plt

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


def create_icon_for_marker(cluster_id):
    """ First implementation with usage database """
    number_of_points = ClusterPoint.query.filter(
        ClusterPoint.cluster_id == cluster_id
    ).count()

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

    return Icon(color=icon_color, icon="gift")


def create_popup_for_marker(cluster_id):
    sources = {"altertravel": 0, "autotravel": 0, "geocaching": 0}

    points = ClusterPoint.query.filter(ClusterPoint.cluster_id == cluster_id)
    for point in points:
        point_object = Point.query.filter(Point.id == point.point_id)
        sources[point_object.first().source] += 1

    alter, auto, geo = (
        sources["altertravel"],
        sources["autotravel"],
        sources["geocaching"],
    )

    text = Html(
        '<img src="/popup.png?geo={}&alter={}&auto={}" alt="popup_pie">'.format(
            geo, alter, auto
        ),
        script=True,
    )

    return Popup(html=text, max_width=400)


def create_pie_chart_figure(geo_count, alter_count, auto_count):
    LABELS = ("geocaching", "altertravel", "autotravel")
    sizes = [geo_count, alter_count, auto_count]
    COLORS = ["lightgreen", "gold", "lightskyblue"]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=LABELS, colors=COLORS, shadow=True, startangle=140)
    return fig


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
