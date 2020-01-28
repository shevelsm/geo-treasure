from os import environ

from celery import Celery
from celery.schedules import crontab

from calculate_clusters import calculate_clusters
from webapp import create_app
from webapp.altravel_points import get_altravel_points
from webapp.autotravel_points import get_autotravel_points
from webapp.geocaching_points import get_geocaching_points


flask_app = create_app()
# Broker: RabbitMQ or Redis
broker_url = environ["GEO_BROKER_URL"]
celery_app = Celery("tasks", broker=broker_url)


@celery_app.task
def update_points_and_clusters():
    with flask_app.app_context():
        get_geocaching_points()
        get_altravel_points()
        get_autotravel_points()
        calculate_clusters()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(0, 0, day_of_month="13"), update_points_and_clusters.s()
    )
