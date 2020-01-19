import logging

import folium
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from webapp.model import Cluster, db, Point
from webapp.utils import (
    add_on_click_handler_to_marker,
    create_icon_for_marker,
    create_popup_for_marker,
)


logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
MAP_START_POSITION = [44.4, 38.75]


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    Bootstrap(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def index():
        # in future get start_position as argument
        folium_map = folium.Map(location=MAP_START_POSITION, zoom_start=8)
        with app.app_context():
            print(Point.__table__)
            points_list = Point.query.with_entities(Point.id, Point.lat, Point.long)
            for point in points_list:
                folium.Marker([point[1], point[2]], popup=point[0]).add_to(folium_map)
        return render_template("index.html", folium_map=folium_map._repr_html_())

    @app.route("/dev")
    def dev():
        folium_map = folium.Map(location=MAP_START_POSITION, zoom_start=8)
        with app.app_context():
            cluster_list = Cluster.query.filter(Cluster.radius == 2.0)
            logging.debug(
                "The number of clusters from the query = {}".format(
                    cluster_list.count()
                )
            )
            for cluster in cluster_list:
                marker = folium.Marker(
                    [cluster.lat, cluster.long],
                    popup=create_popup_for_marker(cluster.id),
                    icon=create_icon_for_marker(cluster.id),
                ).add_to(folium_map)
                add_on_click_handler_to_marker(folium_map, marker, cluster.id)
        return render_template("index.html", folium_map=folium_map._repr_html_())

    @app.route("/devajax/<int:cluster_id>")
    def devajax(cluster_id):
        points = Point.query.filter(Point.clusters.any(cluster_id=cluster_id))
        return render_template("cluster_points.html", points=points)

    return app
