import logging

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint

from webapp import create_app
from webapp.model import Cluster, ClusterPoint, db, Point


logging.basicConfig(
    level=logging.INFO,
    filename="clusters_creating.log",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)


def save_cluster_to_db(lat_cluster, long_cluster, radius_cluster, points_cluster):
    cluster_exist = Cluster.query.filter(
        Cluster.lat == lat_cluster,
        Cluster.long == long_cluster,
        Cluster.radius == radius_cluster,
    ).count()
    logger.debug(f"count this cluster {cluster_exist}")
    if not cluster_exist:
        new_cluster = Cluster(
            lat=lat_cluster, long=long_cluster, radius=radius_cluster,
        )
        db.session.add(new_cluster)
        db.session.commit()
        db.session.refresh(new_cluster)
        logger.debug("New cluster in database id={}".format(new_cluster.id))
        for point in points_cluster:
            new_cluster_point = ClusterPoint(cluster_id=new_cluster.id, point_id=point)
            db.session.add(new_cluster_point)
            db.session.commit()


# Define epsilon list in kilometers, converted to radians for use by haversine
MIN_RADIUS = 2  # [km]
MAX_RADIUS = 10  # [km]
RADIUS_STEP = 2  # [km]
KMS_PER_RADIAN = 6371.0088  # [km]
radius_list = [
    radius for radius in range(MIN_RADIUS, MAX_RADIUS + RADIUS_STEP, RADIUS_STEP)
]
logger.debug("List of radius for clusters {}".format(radius_list))

app = create_app()
with app.app_context():
    con = db.session.bind
    all_points_sql = str(Point.query)
    points_df = pd.read_sql(all_points_sql, con)
    logger.debug(points_df.head())

coords = points_df.as_matrix(columns=["point_lat", "point_long"])

for radius in radius_list:
    logger.info("Creating cluster with R = {} km has been started".format(radius))
    epsilon = radius / KMS_PER_RADIAN
    logger.debug("Epsilon for the current radius is equal {:.5f}".format(epsilon))
    db_scan = DBSCAN(
        eps=epsilon, min_samples=3, algorithm="auto", metric="haversine"
    ).fit(np.radians(coords))
    cluster_labels = db_scan.labels_

    all_labels = set(cluster_labels)
    all_labels.discard(-1)
    num_clusters = len(all_labels)

    logger.info(
        "Clustered {:,} points down to {:,} clusters".format(
            len(points_df), num_clusters
        )
    )

    clusters = [coords[cluster_labels == num] for num in range(num_clusters)]
    points_to_cluster = [
        points_df.point_id[cluster_labels == num] for num in range(num_clusters)
    ]

    logger.info(
        "Writing {} clusters for R = {} km to the database...".format(
            num_clusters, radius
        )
    )
    for num, cluster in enumerate(zip(clusters, points_to_cluster)):
        points_coords, points_id_list = cluster
        lat_cluster = MultiPoint(points_coords).centroid.x
        long_cluster = MultiPoint(points_coords).centroid.y
        logger.debug(
            "Cluster #{} coords: {:.3f}, {:.3f}".format(num, lat_cluster, long_cluster)
        )
        logger.debug("Cluster #{} point list: {}".format(num, list(points_id_list)))
        with app.app_context():
            save_cluster_to_db(
                lat_cluster=lat_cluster,
                long_cluster=long_cluster,
                radius_cluster=radius,
                points_cluster=points_id_list,
            )
