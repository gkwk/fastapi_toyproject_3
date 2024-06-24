from typing import Dict

from database.database import database_dependency
from service.base_update_processor import BaseUpdateProcessor


class BaseUpdateManager:
    def __init__(self):
        self.update_validation_classes: Dict[str, BaseUpdateProcessor] = {}

    def update(self, data_base: database_dependency, model, key: str, value):
        if key in self.update_validation_classes:
            self.update_validation_classes.get(key).validate(
                data_base=data_base, model=model, key=key, value=value
            )
            self.update_validation_classes.get(key).set_value(
                data_base=data_base, model=model, key=key, value=value
            )
