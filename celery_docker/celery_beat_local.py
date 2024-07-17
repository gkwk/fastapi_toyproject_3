from pathlib import Path

from dotenv import load_dotenv

from celery_app import celery_app


if __name__ == '__main__':
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    celery_app.start(["beat", "--loglevel=info"])