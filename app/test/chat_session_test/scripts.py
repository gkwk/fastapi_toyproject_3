from pathlib import Path

import pytest
from httpx import Response
from fastapi import WebSocket
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import Response


from main import app
from test.url_class import ChatSessionURLClass
from test.login_user import LoginUser
from test.parameter_data_loader import parameter_data_loader
from database.database import get_data_base_decorator_v2
from service.chat_session.logic_get_chat_session import logic_get_chat_session

_client = TestClient(app)


class _ChatSessionTestMethods:
    @staticmethod
    def create_chat_session(
        login_user: LoginUser,
        name: str,
        information: str,
        is_visible: bool,
        is_closed: bool,
    ):
        client_response = _client.post(
            ChatSessionURLClass.chat_sessions(),
            json={
                "name": name,
                "information": information,
                "is_visible": is_visible,
                "is_closed": is_closed,
            },
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def create_chat_session_test(
        name: str,
        information: str,
        is_visible: bool,
        is_closed: bool,
        client_response: Response,
        data_base: Session = None,
    ):
        assert client_response.status_code == 201

        response_test_json: dict = client_response.json()
        assert response_test_json.get("result")
        assert response_test_json.get("id")

        post = logic_get_chat_session(
            data_base=data_base, filter_dict={"id": response_test_json.get("id")}
        )
        assert post.name == name
        assert post.information == information
        assert post.is_visible == is_visible
        assert post.is_closed == is_closed

    @staticmethod
    def get_chat_session_list(login_user: LoginUser):
        client_response = _client.get(
            ChatSessionURLClass.chat_sessions(),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def get_chat_session_list_test(
        columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("role")
        assert response_test_json.get("chat_sessions")

        if response_test_json.get("chat_sessions"):
            for chat_session in response_test_json.get("chat_sessions"):
                assert set(columns) == set(chat_session.keys())

    @staticmethod
    def get_chat_session_detail(login_user: LoginUser, chat_session_id: int):
        response_test = _client.get(
            ChatSessionURLClass.chat_sessions_chat_session_id(chat_session_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def get_chat_session_detail_test(
        chat_session_id: int,
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
    def update_chat_session_detail(
        login_user: LoginUser,
        chat_session_id: int,
        patch_json: dict = {},
    ):
        response_test = _client.patch(
            ChatSessionURLClass.chat_sessions_chat_session_id(chat_session_id),
            json=patch_json,
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def update_chat_session_detail_test(
        client_response: Response,
        chat_session_id: int,
        patch_json: dict = {},
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        chat_session = logic_get_chat_session(
            data_base=data_base, filter_dict={"id": chat_session_id}
        )

        if "name" in patch_json:
            assert chat_session.name == patch_json.get("name")
        if "information" in patch_json:
            assert chat_session.information == patch_json.get("information")
        if "is_visible" in patch_json:
            assert chat_session.is_visible == patch_json.get("is_visible")
        if "is_closed" in patch_json:
            assert chat_session.is_closed == patch_json.get("is_closed")

    @staticmethod
    def delete_chat_session(
        login_user: LoginUser,
        chat_session_id: int,
    ):
        response_test = _client.delete(
            ChatSessionURLClass.chat_sessions_chat_session_id(chat_session_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def delete_chat_session_test(
        client_response: Response,
        chat_session_id: int,
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        assert (
            logic_get_chat_session(
                data_base=data_base, filter_dict={"id": chat_session_id}
            )
            == None
        )

    @staticmethod
    def websocket_chat_session(
        login_user: LoginUser,
        chat_session_id: int,
        chat_message: str,
    ):
        assert login_user.get_websocket_access_token() != ""
        # 현재 websocket 접속에 실패하면 pytest가 프리징 되는 문제가 있음. 해결법 탐색이 필요.
        
        with _client.websocket_connect(
            ChatSessionURLClass.chat_sessions_chat_session_id_ws_with_websocket_access_token(
                chat_session_id, login_user.get_websocket_access_token()
            ),
        ) as websocket:
            websocket: WebSocket
            response_receive_test = websocket.receive_json()
            websocket.send_json(
                {"message": chat_message, "access_token": login_user.get_access_token()}
            )
            print(websocket.receive_json())
            websocket.close()

        return response_receive_test


class TestChatSession:
    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/create_chat_session.json"
        )
    )
    def test_create_chat_session(
        pn,
        login_name,
        login_password,
        name: str,
        information: str,
        is_visible: bool,
        is_closed: bool,
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatSessionTestMethods.create_chat_session(
            login_user,
            name,
            information,
            is_visible,
            is_closed,
        )

        _ChatSessionTestMethods.create_chat_session_test(
            name, information, is_visible, is_closed, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_chat_session_list.json"
        )
    )
    def test_get_chat_session_list(pn, login_name, login_password, test_columns):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatSessionTestMethods.get_chat_session_list(login_user)

        _ChatSessionTestMethods.get_chat_session_list_test(
            test_columns, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_chat_session_detail.json"
        )
    )
    def test_get_chat_session_detail(
        pn, login_name, login_password, chat_session_id, test_columns
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatSessionTestMethods.get_chat_session_detail(
            login_user, chat_session_id
        )

        _ChatSessionTestMethods.get_chat_session_detail_test(
            chat_session_id, test_columns, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent
            / "parameters/update_chat_session_detail.json"
        )
    )
    def test_update_chat_session_detail(
        pn, login_name, login_password, chat_session_id: int, patch_json: dict
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatSessionTestMethods.update_chat_session_detail(
            login_user, chat_session_id, patch_json
        )

        _ChatSessionTestMethods.update_chat_session_detail_test(
            client_response, chat_session_id, patch_json
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/delete_chat_session.json"
        )
    )
    def test_delete_chat_session(pn, login_name, login_password, chat_session_id: int):

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatSessionTestMethods.delete_chat_session(
            login_user, chat_session_id
        )

        _ChatSessionTestMethods.delete_chat_session_test(
            client_response, chat_session_id
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/websocket_chat_session.json"
        )
    )
    def test_websocket_chat_session(
        pn, login_name, login_password, chat_session_id: int, chat_message: str
    ):

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _ChatSessionTestMethods.websocket_chat_session(
            login_user, chat_session_id, chat_message
        )
