import os
import time, datetime

from celery import Celery
from celery.schedules import crontab

from celery_app.v1.posts.tasks import update_post_view_counts
from celery_app.v1.ais.tasks import train_ai_task
from celery_app.v1.ailogs.tasks import infer_ai_task


celery_app_result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "db+sqlite:///./volume/database/test.sqlite"
)
celery_app_broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672"
)

celery_app = Celery(
    __name__,
    backend=celery_app_result_backend,
    broker=celery_app_broker_url,
)

celery_app.task(name="update_post_view_counts")(update_post_view_counts)
celery_app.task(name="train_ai_task")(train_ai_task)
celery_app.task(name="infer_ai_task")(infer_ai_task)


celery_app.conf.beat_schedule = {
    "update_post_view_counts": {
        "task": "update_post_view_counts",
        "schedule": 20.0,
        "args": (None,),
    },
}

celery_app.conf.beat_schedule_filename = "./celery_app/beat/celerybeat-schedule"
