from typing import cast
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pickle
from datetime import datetime, UTC

from test.celery_test.rabbitmq_method.rabbitmq_method import send_to_fastapi
from test.celery_test.enums.ai_type import AIType


def load_model(path: str):
    try:
        with open(path, "rb") as model_file:
            return pickle.load(model_file)
    except FileNotFoundError:
        return None


def save_model(path: str, model_object):
    with open(path, "wb") as model_file:
        pickle.dump(model_object, model_file)


def train_ai_task(ai_id: int, ai_name: str, ai_type: AIType, is_visible: bool):
    try:
        data_frame = ""

        if ai_type == AIType.text:
            data_frame = pd.read_csv("volume/staticfile/AI_test.CSV")
        elif ai_type == AIType.image:
            data_frame = pd.read_csv("volume/staticfile/AI_test.CSV")

        x = data_frame.drop("y", axis=1)
        y = data_frame["y"]

        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.3)

        model = LinearRegression()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_val)
        rmse = mean_squared_error(y_val, y_pred) ** 0.5
        print(rmse)

        save_model(f"volume/ai_model_store/{ai_name}_{ai_id}.pkl", model)

        finish_date = datetime.now(tz=UTC)
        is_available = True

        # fastapi로 결과 전송
        send_to_fastapi(
            message={
                "task_key":"train_ai",
                "ai_id": ai_id,
                "finish_date": finish_date,
                "is_available": is_available,
                "is_visible": is_visible,
            },
            json_message=True,
        )

        return "Success"

    except:
        return "Fail"
