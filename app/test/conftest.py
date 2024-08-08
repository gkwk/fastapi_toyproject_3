from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")


import pytest
from celery.contrib.testing.tasks import ping

from test.celery_test.celery_app_worker_for_test import celery_app as docker_celery_app
from test.celery_test.config import get_settings


@pytest.fixture(scope="session")
def celery_app():
    app = docker_celery_app
    app.task(name="celery.ping")(ping)
    return app


@pytest.fixture(scope="session")
def celery_config():
    return {
        # "broker_url": "memory://",
        "broker_url": f"amqp://{get_settings().RABBITMQ_USERNAME}:{get_settings().RABBITMQ_PASSWORD}@{get_settings().RABBITMQ_HOST_NAME}:{get_settings().RABBITMQ_PORT}",
        "result_backend": "cache",
        "cache_backend": "memory",
        "task_always_eager": True,
        "task_eager_propagates": True,
        # "imports": ("celery.contrib.testing.tasks",),
    }
