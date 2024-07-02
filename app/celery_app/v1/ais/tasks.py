from typing import cast
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pickle
from datetime import datetime

from celery import Task
from sqlalchemy.orm import Session

from models import AI
from database.database import get_data_base_decorator


def load_model(path: str):
    try:
        with open(path, "rb") as model_file:
            return pickle.load(model_file)
    except FileNotFoundError:
        return None


def save_model(path: str, model_object):
    with open(path, "wb") as model_file:
        pickle.dump(model_object, model_file)


@get_data_base_decorator
def train_ai_task(data_base: Session, ai_id, is_visible):
    try:
        ai = data_base.query(AI).filter_by(id=ai_id).first()

        data_frame = pd.read_csv("volume/staticfile/AI_test.CSV")
        x = data_frame.drop("y", axis=1)
        y = data_frame["y"]

        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.3)

        model = LinearRegression()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_val)
        rmse = mean_squared_error(y_val, y_pred) ** 0.5
        print(rmse)

        save_model(f"volume/ai_model_store/{ai.name}_{ai.id}.pkl", model)

        ai.finish_date = datetime.now()
        ai.is_available = True
        ai.is_visible = is_visible
        data_base.add(ai)
        data_base.commit()
    except:
        return None


celery_task_ai_train: Task = cast(Task, train_ai_task)
