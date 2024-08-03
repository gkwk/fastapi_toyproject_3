from pathlib import Path

import pytest
from httpx import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from test.url_class import UserURLClass
from test.login_user import LoginUser
from test.parameter_data_loader import parameter_data_loader
from database.database import get_data_base_decorator_v2
from service.user.logic_get_user_with_id import logic_get_user_with_id
from service.user.logic_get_user_with_username import logic_get_user_with_username

_client = TestClient(app)


class _UserTestMethods:
    @staticmethod
    def create_user(name, password1, password2, email):
        client_response = _client.post(
            UserURLClass.user(),
            json={
                "name": name,
                "password1": password1,
                "password2": password2,
                "email": email,
            },
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def create_user_test(
        name,
        password1,
        password2,
        email,
        client_response: Response,
        data_base: Session = None,
    ):
        assert client_response.status_code == 201

        response_test_json: dict = client_response.json()
        assert response_test_json.get("result")
        assert response_test_json.get("id")

        user = logic_get_user_with_id(
            data_base=data_base, user_id=response_test_json.get("id")
        )
        assert user.name == name
        assert user.email == email
        assert user.password != password1
        # password는 login test로 간접 확인한다.

    @staticmethod
    def get_user_list(login_user: LoginUser):
        client_response = _client.get(
            UserURLClass.user(),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def get_user_list_test(
        columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("users")

        if response_test_json.get("users"):
            for user in response_test_json.get("users"):
                assert set(columns) == set(user.keys())

    @staticmethod
    def get_user_detail(login_user: LoginUser, user_id: int):
        response_test = _client.get(
            UserURLClass.user_user_id(user_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def get_user_detail_test(
        columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()

        assert set(columns) == set(response_test_json.keys())

    @staticmethod
    def update_user_detail(
        login_user: LoginUser,
        user_id: int,
        patch_json: dict = {},
    ):
        response_test = _client.patch(
            UserURLClass.user_user_id(user_id),
            json=patch_json,
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def update_user_detail_test(
        login_user: LoginUser,
        client_response: Response,
        user_id: int,
        patch_json: dict = {},
        data_base: Session = None,
    ):

        assert client_response.status_code == 204

        user = logic_get_user_with_username(
            data_base=data_base, name=login_user.username
        )

        if "email" in patch_json:
            assert user.email == patch_json.get("email")
        if ("password1" in patch_json) and ("password2" in patch_json):
            new_login_user = LoginUser(
                _client, login_user.username, patch_json.get("password1")
            )

            assert new_login_user.access_token
            assert new_login_user.refresh_token
            
            
    @staticmethod
    def delete_user(
        login_user: LoginUser,
        user_id: int,
    ):
        response_test = _client.delete(
            UserURLClass.user_user_id(user_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def delete_user_test(
        client_response: Response,
        user_id: int,
        data_base: Session = None,
    ):

        assert client_response.status_code == 204

        assert logic_get_user_with_id(data_base=data_base, user_id=user_id) == None


class TestUser:
    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/create_user.json"
        )
    )
    def test_create_user(pn, name, password1, password2, email):
        client_response = _UserTestMethods.create_user(
            name, password1, password2, email
        )

        _UserTestMethods.create_user_test(
            name, password1, password2, email, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_user_list.json"
        )
    )
    def test_get_user_list(pn, login_name, login_password, test_columns):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _UserTestMethods.get_user_list(login_user)

        _UserTestMethods.get_user_list_test(test_columns, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_user_detail.json"
        )
    )
    def test_get_user_detail(
        pn, login_name, login_password, user_id: int, test_columns
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _UserTestMethods.get_user_detail(login_user, user_id)

        _UserTestMethods.get_user_detail_test(test_columns, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/update_user_detail.json"
        )
    )
    def test_update_user_detail(
        pn, login_name, login_password, user_id: int, patch_json: dict
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _UserTestMethods.update_user_detail(
            login_user, user_id, patch_json
        )

        _UserTestMethods.update_user_detail_test(
            login_user, client_response, user_id, patch_json
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/delete_user.json"
        )
    )
    def test_delete_user(pn, login_name, login_password, user_id: int):

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _UserTestMethods.delete_user(login_user, user_id)

        _UserTestMethods.delete_user_test(client_response, user_id)
