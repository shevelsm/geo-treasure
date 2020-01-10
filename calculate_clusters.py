import logging

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

from webapp import create_app
from webapp.model import Cluster, ClusterPoint, db, Point


logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])


def save_cluster_to_db():
    pass


def save_cluster_to_point_to_db():
    pass


# Define epsilon list in kilometers, converted to radians for use by haversine
# epsilon == diametr == radius * 2
MIN_RADIUS = 5  # [km]
MAX_RADIUS = 20  # [km]
RADIUS_STEP = 5  # [km]
KMS_PER_RADIAN = 6371.0088  # [km]
radius_list = [r for r in range(MIN_RADIUS, MAX_RADIUS + RADIUS_STEP, RADIUS_STEP)]
logging.debug("List of radiuses for clusters {}".format(radius_list))

app = create_app()
with app.app_context():
    con = db.session.bind
    all_points_sql = Point.query.__str__()
    points_df = pd.read_sql(all_points_sql, con)
    logging.debug(points_df.head())

    coords = points_df.as_matrix(columns=["point_lat", "point_long"])
    logging.debug("Matrix representation of points coords:\n{}".format(coords))

    for radius in radius_list:
        logging.info("\nCreating cluster with R = {} km has been started".format(radius))
        epsilon = radius / KMS_PER_RADIAN
        logging.debug("Epsilon for the current radius is equal {:.5f}".format(epsilon))
        db = DBSCAN(
            eps=epsilon, min_samples=1, algorithm="ball_tree", metric="haversine"
        ).fit(np.radians(coords))
        cluster_labels = db.labels_

        num_clusters = len(set(cluster_labels))

        message = "Clustered {:,} points down to {:,} clusters, for {:.1f}% compression"
        logging.debug(
            message.format(
                len(points_df),
                num_clusters,
                100 * (1 - float(num_clusters) / len(points_df)),
            )
        )
        logging.debug(
            "Silhouette coefficient: {:0.03f}".format(
                metrics.silhouette_score(coords, cluster_labels)
            )
        )

        clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])

        for num, cluster in enumerate(clusters):
            cluster_lat = MultiPoint(cluster).centroid.x
            cluster_long = MultiPoint(cluster).centroid.y
            logging.debug(
                "Cluster #{} coords: {:.3f}, {:.3f}".format(num, cluster_lat, cluster_long)
            ) 
