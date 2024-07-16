import contextlib
import os

from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
import asyncio
import aio_pika
from aio_pika.abc import AbstractRobustConnection
import orjson
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError


from database.database import database_engine_shutdown
from logger.logger_methods import log_message
from database.mongodb_method import mongodb_handler
from database.redis_method import redis_handler
from database.database import get_data_base_decorator
from service.post.logic_get_post import logic_get_post
from config.config import get_settings


RABBITMQ_URL = f"amqp://{get_settings().RABBITMQ_USERNAME}:{get_settings().RABBITMQ_PASSWORD}@{get_settings().RABBITMQ_HOST_NAME}:{get_settings().RABBITMQ_PORT}"


from uuid import uuid4
from time import time
from database.redis_method import board_cache_get, post_view_count_cache_set

from service.ai.logic_get_ai_with_id import logic_get_ai_with_id
from service.ailog.logic_get_ailog import logic_get_ailog


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


@get_data_base_decorator
def post_view_db(data_base: Session, message_json: dict):
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


@get_data_base_decorator
def train_ai_db(data_base: Session, message_json: dict):
    ai_id = message_json.get("ai_id")
    finish_date = message_json.get("finish_date")
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
        # raise e
    except IntegrityError as e:
        data_base.rollback()
        # raise e


@get_data_base_decorator
def infer_ai_db(data_base: Session, message_json: dict):
    ai_id = message_json.get("ai_id")
    ailog_id = message_json.get("ailog_id")
    result_mongodb_id = message_json.get("result_mongodb_id")
    finish_date = message_json.get("finish_date")
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


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        message_json = orjson.loads(message.body.decode())
        if message_json.get("task_key") == "update_post_view_counts":
            await run_in_threadpool(post_view_db, None, message_json)
        elif message_json.get("task_key") == "train_ai":
            await run_in_threadpool(train_ai_db, None, message_json)
        elif message_json.get("task_key") == "infer_ai":
            await run_in_threadpool(infer_ai_db, None, message_json)
        else:
            pass


async def rabbitmq_listen(connection: AbstractRobustConnection):
    channel = await connection.channel()
    queue = await channel.declare_queue("fastapi_queue", durable=True)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await process_message(message)


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("lifespan_start")
    log_message(f"SYSTEM | app start")
    rabbitmq_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    rabbitmq_listener = asyncio.create_task(rabbitmq_listen(rabbitmq_connection))

    yield
    print("lifespan_shutdown")
    rabbitmq_listener.cancel()
    log_message(f"SYSTEM | rabbitmq listening asyncio task cancelled")
    await rabbitmq_connection.close()
    log_message(f"SYSTEM | rabbitmq connection close")
    mongodb_handler.close()
    log_message(f"SYSTEM | mongodb connection close")
    redis_handler.close()
    log_message(f"SYSTEM | redis connection close")
    database_engine_shutdown()
    log_message(f"SYSTEM | database shutdown")
    log_message(f"SYSTEM | app shutdown")
