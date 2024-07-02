from fastapi.testclient import TestClient
from sqlalchemy import delete, text

from main import app
from router.v1 import v1_url
from database.database import session_local, engine, MetaData

_client = TestClient(app)


class _MainTestMethods:
    @staticmethod
    def data_base_init():
        data_base = session_local()
        meta_data = MetaData()
        meta_data.reflect(bind=engine)

        for table in reversed(meta_data.sorted_tables):
            if table != meta_data.tables["alembic_version"]:
                data_base.execute(table.delete())

        for value in data_base.execute(text("SELECT * FROM sqlite_sequence")).all():
            data_base.execute(
                text(f'UPDATE sqlite_sequence SET seq = 0 WHERE name = "{value[0]}"')
            )

        data_base.commit()
        data_base.close()

    @staticmethod
    def read_main():
        response = _client.get(
            v1_url.API_V1_ROUTER_PREFIX + v1_url.MAIN_ROUTER_PREFIX + v1_url.ENDPOINT
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, FastAPI!"}


class TestMain:
    def test_data_base_init(self):
        _MainTestMethods.data_base_init()

    def test_read_main(self):
        _MainTestMethods.read_main()
