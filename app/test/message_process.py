from datetime import datetime
from uuid import uuid4
from time import time
import orjson

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
import pika

from database.database import get_data_base_decorator_v2
from database.redis_method import post_view_count_cache_set
from service.ai.logic_get_ai_with_id import logic_get_ai_with_id
from service.post.logic_get_post import logic_get_post
from service.ai.logic_get_ai_with_id import logic_get_ai_with_id
from service.ailog.logic_get_ailog import logic_get_ailog
from test.celery_test.config import get_settings


def record_post_view(
    user_id: int,
    post_id: int,
    count: int,
):
    uuid = str(uuid4())
    timestamp = int(time())
    try:
        post_view_count_cache_set(
            user_id=user_id,
            post_id=post_id,
            uuid=uuid,
            timestamp=timestamp,
            value=str(count),
        )
    except Exception as e:
        pass


@get_data_base_decorator_v2
def post_view_db(message_json: dict, data_base: Session = None):
    post_id = message_json.get("post_id")
    count = message_json.get("count")

    try:
        filter_dict = {
            "id": post_id,
            # "board_id": board_id,
        }

        post = logic_get_post(
            data_base=data_base,
            filter_dict=filter_dict,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )

        if post:
            post.number_of_view = post.number_of_view + count
            data_base.commit()

    except OperationalError as e:
        data_base.rollback()
        record_post_view(user_id=0, post_id=post_id)
        # raise e
    except IntegrityError as e:
        data_base.rollback()
        record_post_view(user_id=0, post_id=post_id)
        # raise e
    finally:
        data_base.refresh(post)


@get_data_base_decorator_v2
def train_ai_db(message_json: dict, data_base: Session = None):
    ai_id = message_json.get("ai_id")
    finish_date = datetime.fromisoformat(message_json.get("finish_date"))
    is_available = message_json.get("is_available")
    is_visible = message_json.get("is_visible")

    try:
        ai = logic_get_ai_with_id(
            data_base=data_base,
            ai_id=ai_id,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )

        if ai:
            ai.finish_date = finish_date
            ai.is_available = is_available
            ai.is_visible = is_visible
            data_base.commit()

    except OperationalError as e:
        data_base.rollback()
        # print(e)
    except IntegrityError as e:
        data_base.rollback()
        # print(e)


@get_data_base_decorator_v2
def infer_ai_db(message_json: dict, data_base: Session = None):
    ai_id = message_json.get("ai_id")
    ailog_id = message_json.get("ailog_id")
    result_mongodb_id = message_json.get("result_mongodb_id")
    finish_date = datetime.fromisoformat(message_json.get("finish_date"))
    is_finished = message_json.get("is_finished")
    try:
        filter_dict = {
            "id": ailog_id,
            "ai_id": ai_id,
        }

        ailog = logic_get_ailog(
            data_base=data_base,
            filter_dict=filter_dict,
            with_for_update=True,
            with_for_update_dict={"nowait": True},
        )

        if ailog:
            ailog.result = result_mongodb_id
            ailog.finish_date = finish_date
            ailog.is_finished = is_finished
            data_base.commit()

    except OperationalError as e:
        data_base.rollback()
        # raise e
    except IntegrityError as e:
        data_base.rollback()
        # raise e


def process_message(body):
    message_json = orjson.loads(body.decode())

    if message_json.get("task_key") == "update_post_view_counts":
        post_view_db(message_json)
    elif message_json.get("task_key") == "train_ai":
        train_ai_db(message_json)
    elif message_json.get("task_key") == "infer_ai":
        infer_ai_db(message_json)
    else:
        pass


def process_rabbitmq_message():
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

    while True:
        method, properties, body = channel.basic_get(
            queue=get_settings().FASTAPI_QUEUE_NAME
        )
        if method:
            process_message(body)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            break

    connection.close()
