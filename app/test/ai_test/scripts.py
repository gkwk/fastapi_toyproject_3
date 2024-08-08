from pathlib import Path

import pytest
from httpx import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import Response

from main import app
from test.url_class import AIURLClass
from test.login_user import LoginUser
from test.parameter_data_loader import parameter_data_loader
from test.message_process import process_rabbitmq_message
from database.database import get_data_base_decorator_v2
from enums.ai_type import AIType
from service.ai.logic_get_ai_with_id import logic_get_ai_with_id


_client = TestClient(app)


class _AITestMethods:
    @staticmethod
    def create_ai(
        login_user: LoginUser,
        name: str,
        description: str,
        is_visible: bool,
        ai_type: AIType,
    ):
        client_response = _client.post(
            AIURLClass.ais(),
            json={
                "name": name,
                "description": description,
                "is_visible": is_visible,
                "ai_type": ai_type,
            },
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def create_ai_test(
        name: str,
        description: str,
        is_visible: bool,
        ai_type: AIType,
        client_response: Response,
        data_base: Session = None,
    ):
        assert client_response.status_code == 202

        response_test_json: dict = client_response.json()
        assert response_test_json.get("task_id")
        assert response_test_json.get("id")

        ai = logic_get_ai_with_id(
            data_base=data_base, ai_id=response_test_json.get("id")
        )

        # db에서 ai를 읽어올 시, 첫 테스트에 사용되는 row의 값이 갱신되지 않는 점을 확인하였음.
        # flush나 expire_all 등을 사용하였지만 해결되지 않음.
        # 문제 해결 방법을 현재는 알 수 없어 test를 분할하였음.
        # test 분할 시 문제가 해결되는 것으로 볼 때, session관리에 문제가 있는 것으로 생각됨.
        # 데코레이터를 수정하는 방법 등을 생각중

        # assert ai.name == name
        # assert ai.description == description
        assert ai.celery_task_id == response_test_json.get("task_id")
        # assert ai.is_visible == is_visible
        # assert ai.ai_type == ai_type

    @staticmethod
    @get_data_base_decorator_v2
    def create_ai_test2(
        name: str,
        description: str,
        is_visible: bool,
        ai_type: AIType,
        ai_id,
        data_base: Session = None,
    ):
        ai = logic_get_ai_with_id(data_base=data_base, ai_id=ai_id)

        assert ai.name == name
        assert ai.description == description
        assert ai.is_visible == is_visible
        assert ai.ai_type == ai_type

    @staticmethod
    def get_ai_list(login_user: LoginUser):
        client_response = _client.get(
            AIURLClass.ais(),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def get_ai_list_test(columns, client_response: Response, data_base: Session = None):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("role")
        assert response_test_json.get("ais")

        if response_test_json.get("ais"):
            for ai in response_test_json.get("ais"):
                assert set(columns) == set(ai.keys())

    @staticmethod
    def get_ai_detail(login_user: LoginUser, ai_id: int):
        response_test = _client.get(
            AIURLClass.ais_ai_id(ai_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def get_ai_detail_test(
        ai_id: int, columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("role")
        assert response_test_json.get("detail")

        assert set(columns) == set(response_test_json.get("detail").keys())

    @staticmethod
    def update_ai_detail(
        login_user: LoginUser,
        ai_id: int,
        patch_json: dict = {},
    ):
        response_test = _client.patch(
            AIURLClass.ais_ai_id(ai_id),
            json=patch_json,
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def update_ai_detail_test(
        login_user: LoginUser,
        client_response: Response,
        ai_id: int,
        patch_json: dict = {},
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        ai = logic_get_ai_with_id(data_base=data_base, ai_id=ai_id)

        if "name" in patch_json:
            assert ai.name == patch_json.get("name")
        if "description" in patch_json:
            assert ai.description == patch_json.get("description")
        if "is_visible" in patch_json:
            assert ai.is_visible == patch_json.get("is_visible")
        if "is_available" in patch_json:
            assert ai.is_available == patch_json.get("is_available")

    @staticmethod
    def delete_ai(
        login_user: LoginUser,
        ai_id: int,
    ):
        response_test = _client.delete(
            AIURLClass.ais_ai_id(ai_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def delete_ai_test(
        client_response: Response,
        ai_id: int,
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        assert logic_get_ai_with_id(data_base=data_base, ai_id=ai_id) == None


class TestAI:
    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/create_ai.json"
        )
    )
    def test_create_ai(
        celery_app,
        celery_worker,
        pn,
        login_name,
        login_password,
        name,
        description,
        is_visible,
        ai_type,
    ):
        celery_worker.reload()

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AITestMethods.create_ai(
            login_user, name, description, is_visible, ai_type
        )

        process_rabbitmq_message()

        _AITestMethods.create_ai_test(
            name, description, is_visible, ai_type, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/create_ai2.json"
        )
    )
    def test_create_ai2(
        celery_app,
        celery_worker,
        pn,
        login_name,
        login_password,
        name,
        description,
        is_visible,
        ai_type,
        ai_id,
    ):
        _AITestMethods.create_ai_test2(name, description, is_visible, ai_type, ai_id)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_ai_list.json"
        )
    )
    def test_get_ai_list(pn, login_name, login_password, test_columns):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AITestMethods.get_ai_list(login_user)

        _AITestMethods.get_ai_list_test(test_columns, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_ai_detail.json"
        )
    )
    def test_get_ai_detail(pn, login_name, login_password, ai_id, test_columns):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AITestMethods.get_ai_detail(login_user, ai_id)

        _AITestMethods.get_ai_detail_test(ai_id, test_columns, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/update_ai_detail.json"
        )
    )
    def test_update_ai_detail(
        pn, login_name, login_password, ai_id: int, patch_json: dict
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AITestMethods.update_ai_detail(login_user, ai_id, patch_json)

        _AITestMethods.update_ai_detail_test(
            login_user, client_response, ai_id, patch_json
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/delete_ai.json"
        )
    )
    def test_delete_ai(pn, login_name, login_password, ai_id: int):

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AITestMethods.delete_ai(login_user, ai_id)

        _AITestMethods.delete_ai_test(client_response, ai_id)
