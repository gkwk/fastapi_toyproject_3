import time
import jwt
from fastapi.testclient import TestClient

from test.url_class import AuthURLClass


class LoginUser:
    def __init__(self, client: TestClient, username, password1):
        self.client = client
        
        self.username = username
        self.password1 = password1

        response = client.post(
            AuthURLClass.auth_login(),
            data={"username": username, "password": password1},
        )
        self.access_token = response.json().get("access_token")
        self.refresh_token = response.cookies.get("refresh_token")

    def get_access_token(self):
        # access_token 사용시 함수를 사용하도록 하고, 그 과정에서 검증을 걸쳐 자동 갱신하도록 한다.
        if self._is_token_expired():
            self._refresh_access_token()
        
        return self.access_token

    def _refresh_access_token(self):
        response = self.client.post(
            AuthURLClass.auth_reissue_access_token(),
            cookies={"refresh_token": self.refresh_token}
        )
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
    
    def _is_token_expired(self):
        try:
            payload = jwt.decode(self.access_token, options={"verify_signature": False})
            exp = int(payload.get("exp"))
            if (exp - int(time.time())) < 10:
                return True
        except Exception:
            return True

        return False

    def get_websocket_access_token(self):
        response = self.client.post(
            AuthURLClass.auth_issue_websocket_access_token(),
            headers={"Authorization": f"Bearer {self.get_access_token()}"}
        )
        if response.status_code == 200:
            return response.json().get("websocket_access_token")
        
        return ""