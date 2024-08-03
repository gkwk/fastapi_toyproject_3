from pathlib import Path

import pytest
from httpx import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import Response

from main import app
from test.url_class import AuthURLClass
from test.login_user import LoginUser
from test.parameter_data_loader import parameter_data_loader
from database.database import get_data_base_decorator_v2

_client = TestClient(app)


class _AuthTestMethods:
    @staticmethod
    def login(login_name, login_password):
        client_response = _client.post(
            AuthURLClass.auth_login(),
            data={"username": login_name, "password": login_password},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def login_test(login_name, client_response: Response, data_base: Session = None):
        assert client_response.status_code == 200

        assert client_response.cookies.get("refresh_token")

        response_test_json: dict = client_response.json()
        assert response_test_json.get("access_token")
        assert response_test_json.get("token_type") == "bearer"

        # 차후 access token의 내용과 test parameter 일치 여부 확인 코드 추가

    @staticmethod
    def logout(login_user: LoginUser):
        client_response = _client.post(
            AuthURLClass.auth_logout(),
            headers={"Authorization": f"Bearer {login_user.access_token}"},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def logout_test(
        login_user: LoginUser, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("result")
        assert response_test_json.get("id")

        new_client_response = _AuthTestMethods.logout(login_user)

        assert new_client_response.status_code != 200

    @staticmethod
    def issue_websocket_access_token(login_user: LoginUser):
        client_response = _client.post(
            AuthURLClass.auth_issue_websocket_access_token(),
            headers={"Authorization": f"Bearer {login_user.access_token}"},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def issue_websocket_access_token_test(
        login_user: LoginUser, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()

        assert response_test_json.get("websocket_access_token")
        assert response_test_json.get("token_type") == "bearer"

        # 차후 websocket access token의 내용과 test parameter 일치 여부 확인 코드 추가

    @staticmethod
    def reissue_access_token(login_user: LoginUser):
        client_response = _client.post(
            AuthURLClass.auth_reissue_access_token(),
            cookies={"refresh_token": login_user.refresh_token},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def reissue_access_token_test(
        login_user: LoginUser, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("access_token")
        assert response_test_json.get("token_type") == "bearer"

        # 차후 access token의 내용과 test parameter 일치 여부 확인 코드 추가
        
        # 기존 access token의 만료 여부 확인
        new_client_response = _AuthTestMethods.logout(login_user)

        assert new_client_response.status_code != 200

    # password_reset test는 차후 추가
    # SMTP를 통한 이메일의 전송 여부 확인 및 전송된 내용을 확인하고 메일 내 포함된 token을 자동으로 추출하여 테스트에 사용하는 방법을 생각해보기
    
    
class TestAuth:
    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/login.json"
        )
    )
    def test_login(pn, login_name, login_password):
        client_response = _AuthTestMethods.login(login_name, login_password)

        _AuthTestMethods.login_test(login_name, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/logout.json"
        )
    )
    def test_logout(pn, login_name, login_password):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AuthTestMethods.logout(login_user)

        _AuthTestMethods.logout_test(login_user, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent
            / "parameters/issue_websocket_access_token.json"
        )
    )
    def test_issue_websocket_access_token(pn, login_name, login_password):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AuthTestMethods.issue_websocket_access_token(login_user)

        _AuthTestMethods.issue_websocket_access_token_test(login_user, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/reissue_access_token.json"
        )
    )
    def test_reissue_access_token(pn, login_name, login_password):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _AuthTestMethods.reissue_access_token(login_user)

        _AuthTestMethods.reissue_access_token_test(login_user, client_response)
