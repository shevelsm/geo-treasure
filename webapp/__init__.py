import json
import os

import folium
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from webapp.model import Cluster, db, Point


def markers_generator():
    """ range - searching radius for places """
    path_to_file = os.path.join("webapp", "data", "ready50dots.json")
    with open(path_to_file, "r", encoding="utf-8") as file:
        markers_data = json.loads(file.read())
    return markers_data


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    Bootstrap(app)

    start_position = [44.4, 39.75]

    @app.route("/")
    def index():
        # in future get start_position as argument
        folium_map = folium.Map(location=start_position, zoom_start=9)
        folium.Marker(start_position, popup="CENTER").add_to(folium_map)
        with app.app_context():
            print(Point.__table__)
            points_list = Point.query.with_entities(Point.id, Point.lat, Point.long)
            for point in points_list:
                folium.Marker([point[1], point[2]], popup=point[0]).add_to(folium_map)
        return render_template("index.html", folium_map=folium_map._repr_html_())

    @app.route("/dev")
    def dev():
        folium_map = folium.Map(location=start_position, zoom_start=9)
        folium.Marker(start_position, popup="CENTER").add_to(folium_map)
        with app.app_context():
            cluster_list = Cluster.query.filter(Cluster.radius == 10.0)
            for cluster in cluster_list:
                folium.Marker(
                    [cluster.lat, cluster.long], popup=cluster.id, icon=None
                ).add_to(folium_map)
        return render_template("index.html", folium_map=folium_map._repr_html_())

    return app
