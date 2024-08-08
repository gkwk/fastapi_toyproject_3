import os
import pika
import orjson

from test.celery_test.config import get_settings


def send_to_fastapi(message, json_message=False):
    if json_message:
        message = orjson.dumps(message)

    credentials = pika.PlainCredentials(
        get_settings().RABBITMQ_USERNAME, get_settings().RABBITMQ_PASSWORD
    )
    parameters = pika.ConnectionParameters(
        get_settings().RABBITMQ_HOST_NAME,
        get_settings().RABBITMQ_PORT,
        "/",
        credentials,
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=get_settings().FASTAPI_QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange="", routing_key=get_settings().FASTAPI_QUEUE_NAME, body=message
    )
    connection.close()
