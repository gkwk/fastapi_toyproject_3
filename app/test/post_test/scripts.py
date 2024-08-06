from pathlib import Path

import pytest
from httpx import Response
from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import Response
from io import BytesIO


from main import app
from test.url_class import PostURLClass
from test.login_user import LoginUser
from test.parameter_data_loader import parameter_data_loader
from database.database import get_data_base_decorator_v2
from service.post.logic_get_post import logic_get_post

_client = TestClient(app)


class _PostTestMethods:
    @staticmethod
    def create_post(
        login_user: LoginUser,
        board_id: int,
        name: str,
        content: str,
        is_visible: bool,
        file_paths: list[str],
    ):
        create_form = {
            "name": name,
            "content": content,
            "is_visible": is_visible,
        }

        files = []

        if file_paths:
            for file_path in file_paths:
                with open(
                    Path(__file__).resolve().parent / f"parameters/{file_path}", "rb"
                ) as file:
                    file_content = file.read()
                    file_name = file_path.split("/")[-1]
                    upload_file = UploadFile(
                        filename=file_name,
                        file=BytesIO(file_content),
                    )
                    # https://www.python-httpx.org/advanced/clients/#multipart-file-encoding
                    files.append(
                        (
                            "files",
                            (
                                upload_file.filename,
                                upload_file.file,
                                upload_file.content_type,
                            ),
                        )
                    )

        client_response = _client.post(
            PostURLClass.posts(board_id),
            data=create_form,
            files=files,
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def create_post_test(
        board_id: int,
        name: str,
        content: str,
        is_visible: bool,
        file_paths: list[str],
        client_response: Response,
        data_base: Session = None,
    ):
        assert client_response.status_code == 201

        response_test_json: dict = client_response.json()
        assert response_test_json.get("result")
        assert response_test_json.get("id")

        post = logic_get_post(
            data_base=data_base, filter_dict={"name": name, "board_id": board_id}
        )
        assert post.name == name
        assert post.content == content
        assert post.is_visible == is_visible

        # 업로드된 file test는 차후 추가
        # name 중복에 대한 test 차후 추가

    @staticmethod
    def get_post_list(login_user: LoginUser, board_id: int):
        client_response = _client.get(
            PostURLClass.posts(board_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return client_response

    @staticmethod
    @get_data_base_decorator_v2
    def get_post_list_test(
        board_id: int, columns, client_response: Response, data_base: Session = None
    ):
        assert client_response.status_code == 200

        response_test_json: dict = client_response.json()
        assert response_test_json.get("role")
        assert response_test_json.get("posts")

        if response_test_json.get("posts"):
            for post in response_test_json.get("posts"):
                assert set(columns) == set(post.keys())

    @staticmethod
    def get_post_detail(login_user: LoginUser, board_id: int, post_id: int):
        response_test = _client.get(
            PostURLClass.posts_post_id(board_id, post_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )
        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def get_post_detail_test(
        board_id: int,
        post_id: int,
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
    def update_post_detail(
        login_user: LoginUser,
        board_id: int,
        post_id: int,
        patch_form: dict = {},
        # 본 test 코드에서는 file_list_append는 list[str] (path)로만 구성되어야 함.
    ):
        files = []

        if patch_form.get("file_list_append"):
            for file_path in patch_form.get("file_list_append"):
                with open(
                    Path(__file__).resolve().parent / f"parameters/{file_path}", "rb"
                ) as file:
                    file_content = file.read()
                    file_name = file_path.split("/")[-1]
                    upload_file = UploadFile(
                        filename=file_name,
                        file=BytesIO(file_content),
                    )
                    # https://www.python-httpx.org/advanced/clients/#multipart-file-encoding
                    files.append(
                        (
                            "file_list_append",
                            (
                                upload_file.filename,
                                upload_file.file,
                                upload_file.content_type,
                            ),
                        )
                    )

        patch_form.pop("file_list_append", None)
        
        response_test = _client.patch(
            PostURLClass.posts_post_id(board_id, post_id),
            data=patch_form,
            files=files,
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def update_post_detail_test(
        client_response: Response,
        board_id: int,
        post_id: int,
        patch_json: dict = {},
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        post = logic_get_post(
            data_base=data_base, filter_dict={"id": post_id, "board_id": board_id}
        )

        if "name" in patch_json:
            assert post.name == patch_json.get("name")
        if "content" in patch_json:
            assert post.content == patch_json.get("content")
        if "is_visible" in patch_json:
            assert post.is_visible == patch_json.get("is_visible")

        # file 추가 및 삭제에 대한 test는 차후 추가. MonkeyPatch로 uuid를 변경
        # name 중복에 대한 test 차후 추가

    @staticmethod
    def delete_post(
        login_user: LoginUser,
        board_id: int,
        post_id: int,
    ):
        response_test = _client.delete(
            PostURLClass.posts_post_id(board_id, post_id),
            headers={"Authorization": f"Bearer {login_user.get_access_token()}"},
        )

        return response_test

    @staticmethod
    @get_data_base_decorator_v2
    def delete_post_test(
        client_response: Response,
        board_id: int,
        post_id: int,
        data_base: Session = None,
    ):
        assert client_response.status_code == 204

        assert (
            logic_get_post(
                data_base=data_base, filter_dict={"id": post_id, "board_id": board_id}
            )
            == None
        )


class TestPost:
    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/create_post.json"
        )
    )
    def test_create_post(
        pn,
        login_name,
        login_password,
        board_id: int,
        name: str,
        content: str,
        is_visible: bool,
        file_paths: list[str],
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _PostTestMethods.create_post(
            login_user,
            board_id,
            name,
            content,
            is_visible,
            file_paths,
        )

        _PostTestMethods.create_post_test(
            board_id, name, content, is_visible, file_paths, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_post_list.json"
        )
    )
    def test_get_post_list(pn, login_name, login_password, board_id, test_columns):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _PostTestMethods.get_post_list(login_user, board_id)

        _PostTestMethods.get_post_list_test(board_id, test_columns, client_response)

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/get_post_detail.json"
        )
    )
    def test_get_post_detail(
        pn, login_name, login_password, board_id, post_id, test_columns
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _PostTestMethods.get_post_detail(
            login_user, board_id, post_id
        )

        _PostTestMethods.get_post_detail_test(
            board_id, post_id, test_columns, client_response
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/update_post_detail.json"
        )
    )
    def test_update_post_detail(
        pn, login_name, login_password, board_id: int, post_id: int, patch_form: dict
    ):
        login_user = LoginUser(_client, login_name, login_password)

        client_response = _PostTestMethods.update_post_detail(
            login_user, board_id, post_id, patch_form
        )

        _PostTestMethods.update_post_detail_test(
            client_response, board_id, post_id, patch_form
        )

    @staticmethod
    @pytest.mark.parametrize(
        **parameter_data_loader(
            Path(__file__).resolve().parent / "parameters/delete_post.json"
        )
    )
    def test_delete_post(pn, login_name, login_password, board_id: int, post_id: int):

        login_user = LoginUser(_client, login_name, login_password)

        client_response = _PostTestMethods.delete_post(login_user, board_id, post_id)

        _PostTestMethods.delete_post_test(client_response, board_id, post_id)
