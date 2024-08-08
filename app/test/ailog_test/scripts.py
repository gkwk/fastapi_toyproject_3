from pathlib import Path

import pytest
from httpx import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import Response

from main import app
from test.url_class import AILogURLClass
from test.login_user import LoginUser
from test.parameter_data_loader import parameter_data_loader
from test.message_process import process_rabbitmq_message
from database.database import get_data_base_decorator_v2
from enums.ai_type import AIType
from service.ailog.logic_get_ailog import logic_get_ailog


_client = TestClient(app)


class _AILogTestMethods:
    @staticmethod
    def create_ailog(login_user: LoginUser, ai_id: int, description: str):
        client_response = _client.post(
            AILogURLClass.ailogs(ai_id),
            json={"description": description},
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def create_ailog_test(
        ai_id: int,
        description: str,
        client_response: Response,
        data_base: Session = None,
    ):
        assert client_response.status_code == 202

        response_test_json: dict = client_response.json()
        assert response_test_json.get("task_id")
        assert response_test_json.get("id")

        ailog = logic_get_ailog(
            data_base=data_base,
            filter_dict={"id": response_test_json.get("id"), "ai_id": ai_id},
        )

        assert ailog.description == description
        assert ailog.celery_task_id == response_test_json.get("task_id")

    @staticmethod
    def get_ailog_list(login_user: LoginUser, ai_id: int):
        client_response = _client.get(
            AILogURLClass.ailogs(ai_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def get_ailog_list_test(
        ai_id: int, columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("role")
        assert response_test_json.get("ailogs")

        if response_test_json.get("ailogs"):
            for ai in response_test_json.get("ailogs"):
                assert set(columns) == set(ai.keys())

    @staticmethod
    def get_ailog_detail(login_user: LoginUser, ai_id: int, ailog_id: int):
        response_test = _client.get(
            AILogURLClass.ailogs_ailog_id(ai_id, ailog_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def get_ailog_detail_test(
        ai_id: int,
        ailog_id: int,
        columns,
        client_response: Response,
        data_base: Session = None,
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("role")
        assert response_test_json.get("detail")

        assert set(columns) == set(response_test_json.get("detail").keys())

    @staticmethod
    def update_ailog_detail(
        login_user: LoginUser,
        ai_id: int,
        ailog_id: int,
        patch_json: dict = {},
    ):
        response_test = _client.patch(
            AILogURLClass.ailogs_ailog_id(ai_id, ailog_id),
            json=patch_json,
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def update_ailog_detail_test(
        login_user: LoginUser,
        client_response: Response,
        ai_id: int,
        ailog_id: int,
        patch_json: dict = {},
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        ailog = logic_get_ailog(
            data_base=data_base, filter_dict={"id": ailog_id, "ai_id": ai_id}
        )

        if "description" in patch_json:
            assert ailog.description == patch_json.get("description")

    @staticmethod
    def delete_ailog(
        login_user: LoginUser,
        ai_id: int,
        ailog_id: int,
    ):
        response_test = _client.delete(
            AILogURLClass.ailogs_ailog_id(ai_id, ailog_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def delete_ailog_test(
        client_response: Response,
        ai_id: int,
        ailog_id: int,
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        assert (
            logic_get_ailog(
                data_base=data_base, filter_dict={"id": ailog_id, "ai_id": ai_id}
            )
            == None
        )


class TestAILog:
    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/create_ailog.json"
        )
    )
    def test_create_ailog(
        celery_app,
        celery_worker,
        pn,
        login_name,
        login_password,
        ai_id,
        description,
    ):
        celery_worker.reload()

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AILogTestMethods.create_ailog(login_user, ai_id, description)

        process_rabbitmq_message()

        _AILogTestMethods.create_ailog_test(ai_id, description, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_ailog_list.json"
        )
    )
    def test_get_ailog_list(pn, login_name, login_password, ai_id, test_columns):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AILogTestMethods.get_ailog_list(login_user, ai_id)

        _AILogTestMethods.get_ailog_list_test(ai_id, test_columns, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_ailog_detail.json"
        )
    )
    def test_get_ailog_detail(
        pn, login_name, login_password, ai_id, ailog_id, test_columns
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AILogTestMethods.get_ailog_detail(
            login_user, ai_id, ailog_id
        )

        _AILogTestMethods.get_ailog_detail_test(
            ai_id, ailog_id, test_columns, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/update_ailog_detail.json"
        )
    )
    def test_update_ailog_detail(
        pn, login_name, login_password, ai_id: int, ailog_id: int, patch_json: dict
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AILogTestMethods.update_ailog_detail(
            login_user, ai_id, ailog_id, patch_json
        )

        _AILogTestMethods.update_ailog_detail_test(
            login_user, client_response, ai_id, ailog_id, patch_json
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/delete_ailog.json"
        )
    )
    def test_delete_ailog(pn, login_name, login_password, ai_id: int, ailog_id: int):

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AILogTestMethods.delete_ailog(login_user, ai_id, ailog_id)

        _AILogTestMethods.delete_ailog_test(client_response, ai_id, ailog_id)
