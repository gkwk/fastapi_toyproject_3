from pathlib import Path

import pytest
from httpx import Response
from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import Response
from io import BytesIO


from main import app
from test.url_class import ChatURLClass
from test.login_user import LoginUser
from test.parameter_data_loader import parameter_data_loader
from database.database import get_data_base_decorator_v2
from service.chat.logic_get_chat import logic_get_chat

_client = TestClient(app)


class _ChatTestMethods:
    @staticmethod
    def get_chat_list(login_user: LoginUser, chat_session_id: int):
        client_response = _client.get(
            ChatURLClass.chats(chat_session_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def get_chat_list_test(
        chat_session_id, columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()

        assert response_test_json.get("role")
        assert "chats" in response_test_json

        if response_test_json.get("chats"):
            for chat_session in response_test_json.get("chats"):
                assert set(columns) == set(chat_session.keys())

    @staticmethod
    def get_chat_detail(login_user: LoginUser, chat_session_id: int, chat_id: int):
        response_test = _client.get(
            ChatURLClass.chats_chat_id(chat_session_id, chat_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def get_chat_detail_test(
        chat_session_id: int,
        chat_id: int,
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
    def delete_chat(
        login_user: LoginUser,
        chat_session_id: int,
        chat_id: int,
    ):
        response_test = _client.delete(
            ChatURLClass.chats_chat_id(chat_session_id, chat_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def delete_chat_test(
        client_response: Response,
        chat_session_id: int,
        chat_id: int,
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        assert (
            logic_get_chat(
                data_base=data_base,
                filter_dict={"id": chat_id, "chat_session_id": chat_session_id},
            )
            == None
        )


class TestChat:
    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_chat_list.json"
        )
    )
    def test_get_chat_list(
        pn, login_name, login_password, chat_session_id, test_columns
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatTestMethods.get_chat_list(login_user, chat_session_id)

        _ChatTestMethods.get_chat_list_test(
            chat_session_id, test_columns, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_chat_detail.json"
        )
    )
    def test_get_chat_session_detail(
        pn, login_name, login_password, chat_session_id, chat_id, test_columns
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatTestMethods.get_chat_detail(
            login_user, chat_session_id, chat_id
        )

        _ChatTestMethods.get_chat_detail_test(
            chat_session_id, chat_id, test_columns, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/delete_chat.json"
        )
    )
    def test_delete_chat_session(
        pn, login_name, login_password, chat_session_id: int, chat_id: int
    ):

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatTestMethods.delete_chat(
            login_user, chat_session_id, chat_id
        )

        _ChatTestMethods.delete_chat_test(client_response, chat_session_id, chat_id)
