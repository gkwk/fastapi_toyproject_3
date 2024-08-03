from router.v1 import v1_url


def url_join(url_list: list[str]) -> str:
    return "".join(url_list)


class MainURLClass:
    @staticmethod
    def index():
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.MAIN_ROUTER_PREFIX,
                v1_url.ENDPOINT,
            ]
        )


class AuthURLClass:
    @staticmethod
    def auth():
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.AUTH_ROUTER_PREFIX,
                v1_url.ENDPOINT,
            ],
        )

    @staticmethod
    def auth_login():
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.AUTH_ROUTER_PREFIX,
                v1_url.AUTH_LOGIN_ROUTER_PREFIX,
                v1_url.ENDPOINT,
            ]
        )

    @staticmethod
    def auth_logout():
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.AUTH_ROUTER_PREFIX,
                v1_url.AUTH_LOGOUT_ROUTER_PREFIX,
                v1_url.ENDPOINT,
            ]
        )

    @staticmethod
    def auth_issue_websocket_access_token():
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.AUTH_ROUTER_PREFIX,
                v1_url.AUTH_ISSUE_WEBSOCKET_ACCESS_TOKEN_ROUTER_PREFIX,
                v1_url.ENDPOINT,
            ]
        )

    @staticmethod
    def auth_reissue_access_token():
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.AUTH_ROUTER_PREFIX,
                v1_url.AUTH_REISSUE_ACCESS_TOKEN_ROUTER_PREFIX,
                v1_url.ENDPOINT,
            ]
        )

    @staticmethod
    def auth_password_reset():
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.AUTH_ROUTER_PREFIX,
                v1_url.AUTH_PASSWORD_RESET_ROUTER_PREFIX,
                v1_url.ENDPOINT,
            ]
        )

    @staticmethod
    def auth_password_reset_token(password_reset_token: str):
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.AUTH_ROUTER_PREFIX,
                v1_url.AUTH_PASSWORD_RESET_ROUTER_PREFIX,
                # v1_url.AUTH_PASSWORD_RESET_TOKEN_ROUTER_PREFIX,
                f"/{password_reset_token}",
                v1_url.ENDPOINT,
            ]
        )


class UserURLClass:
    @staticmethod
    def user():
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.USERS_ROUTER_PREFIX,
                v1_url.ENDPOINT,
            ],
        )

    @staticmethod
    def user_user_id(user_id: int):
        return url_join(
            [
                v1_url.API_V1_ROUTER_PREFIX,
                v1_url.USERS_ROUTER_PREFIX,
                # v1_url.USERS_ID_ROUTER_PREFIX,
                f"/{user_id}",
                v1_url.ENDPOINT,
            ],
        )
