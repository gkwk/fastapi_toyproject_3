import os
import pytest


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "memory://",
        "result_backend": "cache",
        "cache_backend": "memory",
        "task_always_eager": True,
        "task_eager_propagates": True,
    }
