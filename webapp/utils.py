import logging

from folium import Icon

from webapp.model import db, Point, ClusterPoint


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


def create_icon_for_cluster(cluster_id):
    """ First implementation with usage database """
    number_of_points = ClusterPoint.query.filter(
        ClusterPoint.cluster_id == cluster_id).count()
    
    if number_of_points < 5:
        icon_color = 'blue'
    elif number_of_points < 7:
        icon_color = 'pink'
    elif number_of_points < 14:
        icon_color = 'purple'
    elif number_of_points < 36:
        icon_color = 'red'
    else:
        icon_color = 'darkred'

    return Icon(color=icon_color, icon='gift')