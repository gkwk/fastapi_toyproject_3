from celery_app_worker import celery_app


if __name__ == '__main__':
    celery_app.worker_main(["worker", "--loglevel=info", "--pool=solo"])