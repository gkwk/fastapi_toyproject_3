import os
import time, datetime

from celery import Celery
from celery.schedules import crontab

from config import get_settings


celery_app_result_backend = f"db+sqlite:///./volume/database/{get_settings().CELERY_RESULT_BACKEND_FILE_NAME}.sqlite"
celery_app_broker_url = f"amqp://{get_settings().RABBITMQ_USERNAME}:{get_settings().RABBITMQ_PASSWORD}@{get_settings().RABBITMQ_HOST_NAME}:{get_settings().RABBITMQ_PORT}"

celery_app = Celery(
    __name__,
    backend=celery_app_result_backend,
    broker=celery_app_broker_url,
)


celery_app.conf.beat_schedule = {
    "update_post_view_counts": {
        "task": "update_post_view_counts",
        "schedule": 20.0,
        "args": (),
    },
}

celery_app.conf.beat_schedule_filename = "./beat/celerybeat-schedule"
