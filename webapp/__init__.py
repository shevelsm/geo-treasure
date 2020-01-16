import json
import logging
import os

from branca.element import Element
import folium
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from webapp.model import Cluster, db, Point


logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])
MAP_START_POSITION = [44.4, 39.75]


def markers_generator():
    """ range - searching radius for places """
    path_to_file = os.path.join("webapp", "data", "ready50dots.json")
    with open(path_to_file, "r", encoding="utf-8") as file:
        markers_data = json.loads(file.read())
    return markers_data


def add_on_click_handler_to_marker(folium_map, marker, cluster_id):
    my_js = """
            {0}.on('click', function(e) {{
            console.log(e.latlng);
            console.log({1})
            }});
            """.format(
        marker.get_name(),
        cluster_id
    )
    e = Element(my_js)
    html = folium_map.get_root()
    html.script.get_root().render()
    html.script._children[e.get_name()] = e


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    Bootstrap(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def index():
        # in future get start_position as argument
        folium_map = folium.Map(location=MAP_START_POSITION, zoom_start=9)
        with app.app_context():
            print(Point.__table__)
            points_list = Point.query.with_entities(Point.id, Point.lat, Point.long)
            for point in points_list:
                folium.Marker([point[1], point[2]], popup=point[0]).add_to(folium_map)
        return render_template("index.html", folium_map=folium_map._repr_html_())

    @app.route("/dev")
    def dev():
        folium_map = folium.Map(location=MAP_START_POSITION, zoom_start=9)
        with app.app_context():
            cluster_list = Cluster.query.filter(Cluster.radius == 10.0)
            for cluster in cluster_list:
                marker = folium.Marker(
                    [cluster.lat, cluster.long], popup=cluster.id, icon=None
                ).add_to(folium_map)
                add_on_click_handler_to_marker(folium_map, marker, cluster.id)
        return render_template("index.html", folium_map=folium_map._repr_html_())

    return app
