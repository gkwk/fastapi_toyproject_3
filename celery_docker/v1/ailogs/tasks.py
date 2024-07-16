import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
from datetime import datetime, UTC

from rabbitmq_method.rabbitmq_method import send_to_fastapi
from mongodb_method.mongodb_method import mongodb_handler
from enums.ai_type import AIType


def load_model(path: str):
    try:
        with open(path, "rb") as model_file:
            return pickle.load(model_file)
    except FileNotFoundError:
        return None


def save_model(path: str, model_object):
    with open(path, "wb") as model_file:
        pickle.dump(model_object, model_file)


def infer_ai_task(ai_id: int, ai_name: str, ai_type: AIType, ailog_id: int):
    try:
        data_frame = ""

        if ai_type == AIType.text:
            data_frame = pd.read_csv("volume/staticfile/AI_test.CSV")
        elif ai_type == AIType.image:
            data_frame = pd.read_csv("volume/staticfile/AI_test.CSV")

        x = data_frame.drop("y", axis=1)
        y = data_frame["y"]

        model: LinearRegression = load_model(
            f"volume/ai_model_store/{ai_name}_{ai_id}.pkl"
        )
        y_pred = model.predict(x)
        rmse = mean_squared_error(y, y_pred) ** 0.5

        result_dict = {}

        if ai_type == AIType.text:
            result_dict["ai_id"] = ai_id
            result_dict["ailog_id"] = ailog_id
            result_dict["result"] = rmse
            result_dict["type"] = "text"
            result_dict["system"] = "text"
            result_dict["user"] = "text"
            result_dict["assistant"] = "text"

        elif ai_type == AIType.image:
            result_dict["ai_id"] = ai_id
            result_dict["ailog_id"] = ailog_id
            result_dict["result"] = rmse
            result_dict["type"] = "image"
            result_dict["postive_prompt"] = "image"
            result_dict["negative_prompt"] = "image"

        finish_date = datetime.now(tz=UTC)
        is_finished = True

        # mongodb에 결과값 저장
        result_mongodb_id = mongodb_handler.set(value=result_dict)

        # fastapi로 결과 전송
        send_to_fastapi(
            message={
                "task_key": "infer_ai",
                "ai_id": ai_id,
                "ailog_id": ailog_id,
                "result_mongodb_id": result_mongodb_id,
                "finish_date": finish_date,
                "is_finished": is_finished,
            },
            json_message=True,
        )

        return "Success"

    except:
        return "Fail"
