import os

from pymongo import MongoClient
from bson.objectid import ObjectId

from config import get_settings

MONGODB_URL = ""

if (get_settings().MONGODB_USERNAME == None) or (
    get_settings().MONGODB_PASSWORD == None
):
    MONGODB_URL = (
        f"mongodb://{get_settings().MONGODB_HOST_NAME}:{get_settings().MONGODB_PORT}"
    )
else:
    MONGODB_URL = f"mongodb://{get_settings().MONGODB_USERNAME}:{get_settings().MONGODB_PASSWORD}@{get_settings().MONGODB_HOST_NAME}:{get_settings().MONGODB_PORT}"

class MongoDBHandler:
    def __init__(self):
        self._client = MongoClient(MONGODB_URL)
        self._data_base = self._client.get_database("toy_project_mongodb")
        self._ailog_results_collection = self._data_base.get_collection("ailog_results")

    def get(self, key: str):
        bson = self._ailog_results_collection.find_one({"_id": ObjectId(key)})
        return bson

    def set(self, value: dict) -> str:
        result = self._ailog_results_collection.insert_one(value)
        return str(result.inserted_id)

    def delete(self, key: str) -> None:
        self._ailog_results_collection.delete_one({"_id": ObjectId(key)})

    def exist(self, key: str) -> bool:
        bson = self._ailog_results_collection.find_one({"_id": ObjectId(key)})

        if bson:
            return True
        else:
            return False

    def close(self):
        if self._client:
            self._client.close()


mongodb_handler = MongoDBHandler()
