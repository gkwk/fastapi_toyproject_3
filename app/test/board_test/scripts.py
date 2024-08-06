from pathlib import Path

import pytest
from httpx import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import Response

from main import app
from test.url_class import BoardURLClass
from test.login_user import LoginUser
from test.parameter_data_loader import parameter_data_loader
from database.database import get_data_base_decorator_v2
from service.board.logic_get_board import logic_get_board

_client = TestClient(app)


class _BoardTestMethods:
    @staticmethod
    def create_board(
        login_user: LoginUser,
        name: str,
        information: str,
        is_visible: bool,
        is_available: bool,
        user_id_list: list | None,
    ):
        create_json = {
            "name": name,
            "information": information,
            "is_visible": is_visible,
            "is_available": is_available,
        }

        if user_id_list:
            create_json["user_id_list"] = user_id_list

        client_response = _client.post(
            BoardURLClass.boards(),
            json=create_json,
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def create_board_test(
        name: str,
        information: str,
        is_visible: bool,
        is_available: bool,
        user_id_list: list | None,
        client_response: Response,
        data_base: Session = None,
    ):
        assert client_response.status_code == 201

        response_test_json: dict = client_response.json()
        assert response_test_json.get("result")
        assert response_test_json.get("id")

        board = logic_get_board(data_base=data_base, filter_dict={"name": name})
        assert board.name == name
        assert board.information == information
        assert board.is_visible == is_visible
        assert board.is_available == is_available

        # user id list test는 차후 추가

    @staticmethod
    def get_board_list(login_user: LoginUser):
        client_response = _client.get(
            BoardURLClass.boards(),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def get_board_list_test(
        columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("role")
        assert response_test_json.get("boards")

        if response_test_json.get("boards"):
            for board in response_test_json.get("boards"):
                assert set(columns) == set(board.keys())

    @staticmethod
    def get_board_detail(login_user: LoginUser, board_id: int):
        response_test = _client.get(
            BoardURLClass.boards_board_id(board_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def get_board_detail_test(
        columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("role")
        assert response_test_json.get("detail")

        assert set(columns) == set(response_test_json.get("detail").keys())

    @staticmethod
    def update_board_detail(
        login_user: LoginUser,
        board_id: int,
        patch_json: dict = {},
    ):
        response_test = _client.patch(
            BoardURLClass.boards_board_id(board_id),
            json=patch_json,
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def update_board_detail_test(
        client_response: Response,
        board_id: int,
        patch_json: dict = {},
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        board = logic_get_board(data_base=data_base, filter_dict={"id": board_id})

        if "name" in patch_json:
            assert board.name == patch_json.get("name")
        if "information" in patch_json:
            assert board.information == patch_json.get("information")
        if "is_visible" in patch_json:
            assert board.is_visible == patch_json.get("is_visible")
        if "is_available" in patch_json:
            assert board.is_available == patch_json.get("is_available")

        # user id list test는 차후 추가

    @staticmethod
    def delete_board(
        login_user: LoginUser,
        board_id: int,
    ):
        response_test = _client.delete(
            BoardURLClass.boards_board_id(board_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def delete_board_test(
        client_response: Response,
        board_id: int,
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        assert (
            logic_get_board(data_base=data_base, filter_dict={"id": board_id}) == None
        )


class TestBoard:
    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/create_board.json"
        )
    )
    def test_create_board(
        pn,
        login_name,
        login_password,
        name: str,
        information: str,
        is_visible: bool,
        is_available: bool,
        user_id_list: list | None,
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _BoardTestMethods.create_board(
            login_user, name, information, is_visible, is_available, user_id_list
        )

        _BoardTestMethods.create_board_test(
            name, information, is_visible, is_available, user_id_list, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_board_list.json"
        )
    )
    def test_get_board_list(pn, login_name, login_password, test_columns):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _BoardTestMethods.get_board_list(login_user)

        _BoardTestMethods.get_board_list_test(test_columns, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_board_detail.json"
        )
    )
    def test_get_board_detail(pn, login_name, login_password, board_id, test_columns):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _BoardTestMethods.get_board_detail(login_user, board_id)

        _BoardTestMethods.get_board_detail_test(test_columns, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/update_board_detail.json"
        )
    )
    def test_update_board_detail(
        pn, login_name, login_password, board_id: int, patch_json: dict
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _BoardTestMethods.update_board_detail(
            login_user, board_id, patch_json
        )

        _BoardTestMethods.update_board_detail_test(
            client_response, board_id, patch_json
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/delete_board.json"
        )
    )
    def test_delete_board(pn, login_name, login_password, board_id: int):

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _BoardTestMethods.delete_board(login_user, board_id)

        _BoardTestMethods.delete_board_test(client_response, board_id)
