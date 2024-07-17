from celery_app_beat import celery_app


if __name__ == '__main__':
    celery_app.start(["beat", "--loglevel=info"])