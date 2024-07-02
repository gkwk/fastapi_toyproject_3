from pytest import MonkeyPatch

from fastapi.testclient import TestClient

from main import app


_client = TestClient(app)


class _MainTestMethods:
    @staticmethod
    def data_base_init():
        pass

    @staticmethod
    def patch():
        def patch_task():
            a = input()
            b = input()
            return (a, b)

        fake_input = iter(["13", "39", "44", "df"]).__next__
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr("builtins.input", fake_input)

        assert patch_task() == ("13", "39")
        assert patch_task() == ("44", "df")

    @staticmethod
    def add_task(celery_app, celery_worker):
        @celery_app.task
        def mul(x, y):
            return x * y

        celery_worker.reload()
        assert mul.delay(2, 2).get() == 4

    @staticmethod
    def read_main():
        response = _client.get("/api/v1")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, FastAPI!"}


class TestMain:
    def test_patch(self):
        _MainTestMethods.patch()

    def test_add_task(self, celery_app, celery_worker):
        _MainTestMethods.add_task(celery_app=celery_app, celery_worker=celery_worker)

    def test_data_base_init(self):
        _MainTestMethods.data_base_init()

    def test_read_main(self):
        _MainTestMethods.read_main()
