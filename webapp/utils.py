import logging

from webapp.model import db, Point, Cluster, ClusterPoint


def save_point_to_db(title, source, url, lat, long, info):
    point_exists = Point.query.filter(Point.url == url).count()
    logging.debug(f"count this point {point_exists}")
    if not point_exists:
        point = Point(
            title=title, 
            source=source,
            url=url,
            lat=lat,
            long=long,
            info=info,
        )
        db.session.add(point)
        db.session.commit()


def create_icon_for_cluster(cluster):
    pass