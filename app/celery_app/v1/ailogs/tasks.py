from typing import cast

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pickle
import uuid as UUID
import json
from datetime import datetime

from celery import Task

from celery_app.celery import celery_app
from sqlalchemy.orm import Session

from models import AI, AIlog
from database.database import get_data_base_decorator


json_encoder = json.JSONEncoder()
json_decoder = json.JSONDecoder()


def load_model(path: str):
    try:
        with open(path, "rb") as model_file:
            return pickle.load(model_file)
    except FileNotFoundError:
        return None


def save_model(path: str, model_object):
    with open(path, "wb") as model_file:
        pickle.dump(model_object, model_file)


@celery_app.task(name="infer_ai_task")
@get_data_base_decorator
def infer_ai_task(data_base: Session, ailog_id: int, ai_id: int):
    try:
        data_frame = pd.read_csv("volume/staticfile/AI_test.CSV")
        x = data_frame.drop("y", axis=1)
        y = data_frame["y"]

        ai = data_base.query(AI).filter_by(id=ai_id).first()
        model: LinearRegression = load_model(
            f"volume/ai_model_store/{ai.name}_{ai.id}.pkl"
        )
        y_pred = model.predict(x)
        rmse = mean_squared_error(y, y_pred, squared=False)

        ai_log = data_base.query(AIlog).filter_by(id=ailog_id).first()

        result = json_decoder.decode(ai_log.result)
        result["result"] = rmse
        ai_log.result = json_encoder.encode(result)
        ai_log.finish_date = datetime.now()
        ai_log.is_finished = True

        data_base.add(ai_log)
        data_base.commit()
    except:
        return None


celery_task_ai_infer: Task = cast(Task, infer_ai_task)
