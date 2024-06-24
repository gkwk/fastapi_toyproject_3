from abc import ABC, abstractmethod

from database.database import database_dependency


class BaseUpdateProcessor(ABC):
    @abstractmethod
    def validate(self, data_base: database_dependency, model, key: str, value):
        pass

    @abstractmethod
    def set_value(self, data_base: database_dependency, model, key: str, value):
        pass
