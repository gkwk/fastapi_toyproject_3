from pathlib import Path

from dotenv import load_dotenv

from celery_app_worker import celery_app


if __name__ == '__main__':
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    celery_app.worker_main(["worker", "--loglevel=info", "--pool=solo"])