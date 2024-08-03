import inspect

from fastapi.testclient import TestClient
from sqlalchemy import delete, text
from sqlalchemy.orm import Session

from main import app
from database.database import engine, MetaData, Base, get_data_base_decorator_v2
import models
from test.url_class import MainURLClass


_client = TestClient(app)


class _MainTestMethods:
    @staticmethod
    @get_data_base_decorator_v2
    def data_base_init(data_base: Session = None):
        meta_data = MetaData()
        meta_data.reflect(bind=engine)

        for table in reversed(meta_data.sorted_tables):
            if table != meta_data.tables["alembic_version"]:
                data_base.execute(table.delete())

        for value in data_base.execute(text("SELECT * FROM sqlite_sequence")).all():
            data_base.execute(
                text(f'UPDATE sqlite_sequence SET seq = 0 WHERE name = "{value[0]}"')
            )

        for name, model in inspect.getmembers(models, inspect.isclass):
            model: Base
            data_base.execute(delete(model))

        data_base.commit()

    @staticmethod
    def read_main():
        response = _client.get(MainURLClass.index())
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, FastAPI!"}


class TestMain:
    def test_data_base_init(self):
        _MainTestMethods.data_base_init()

    def test_read_main(self):
        _MainTestMethods.read_main()
