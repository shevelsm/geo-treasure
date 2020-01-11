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


def save_cluster_to_db(cluster_lat, cluster_long, cluster_radius, cluster_points):
    pass


# Define epsilon list in kilometers, converted to radians for use by haversine
MIN_DISTANCE = 5  # [km]
MAX_DISTANCE = 5  # [km]
DISTANCE_STEP = 5  # [km]
KMS_PER_RADIAN = 6371.0088  # [km]
distance_list = [
    r for r in range(MIN_DISTANCE, MAX_DISTANCE + DISTANCE_STEP, DISTANCE_STEP)
]
logging.debug("List of distances for clusters {}".format(distance_list))

app = create_app()
with app.app_context():
    con = db.session.bind
    all_points_sql = Point.query.__str__()
    points_df = pd.read_sql(all_points_sql, con)
    logging.debug(points_df.head())

coords = points_df.as_matrix(columns=["point_lat", "point_long"])
logging.debug("Matrix representation of points coords:\n{}".format(coords))

for distance in distance_list:
    logging.info("\nCreating cluster with R = {} km has been started".format(distance))
    epsilon = distance / KMS_PER_RADIAN
    logging.debug("Epsilon for the current distance is equal {:.5f}".format(epsilon))
    db = DBSCAN(
        eps=epsilon, min_samples=3, algorithm="auto", metric="haversine"
    ).fit(np.radians(coords))
    cluster_labels = db.labels_

    all_lables = set(cluster_labels)
    all_lables.discard(-1)
    num_clusters = len(all_lables)

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
    points_to_cluster = [points_df.point_id[cluster_labels == n] for n in range(num_clusters)]

    for num, cluster in enumerate(zip(clusters, points_to_cluster)):
        points_coords, points_id_list = cluster
        cluster_lat = MultiPoint(points_coords).centroid.x
        cluster_long = MultiPoint(points_coords).centroid.y
        logging.debug(
            "Cluster #{} coords: {:.3f}, {:.3f}".format(num, cluster_lat, cluster_long)
        )
        logging.debug(
            "Cluster #{} point list: {}".format(num, list(points_id_list))
        )
