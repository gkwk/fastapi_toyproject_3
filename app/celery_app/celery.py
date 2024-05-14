import os
import time, datetime

from celery import Celery
from celery.schedules import crontab

from models import *

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

from celery_app.v1 import * # 순환 참조 오류 해결을 위한 import 위치 조정

celery_app.autodiscover_tasks([])
