from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import os
import time


from database.redis_method import download_file_lock_cache_set
from auth.jwt.access_token.get_user_access_token_payload import (
    current_user_access_token_payload,
)


def iterate_file_chunk(file_path: str):
    try:
        with open(file_path, "rb") as file:
            start_time = time.time()
            timeout = 30 * 24 * 60 * 60  # 최대 다운로드 타임아웃 30일
            while chunk := file.read(1024 * 8):
                if time.time() - start_time > timeout:
                    raise HTTPException(status_code=408, detail="타임아웃")
                yield chunk

    except HTTPException as e:
        raise e


def http_get(file_id: str, token: current_user_access_token_payload):
    try:
        file_path = os.path.join("volume/staticfile", file_id)

        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

        download_file_lock_cache_set(file_id)
        # 차후 query에 jwt를 포함시켜 access token의 user id와의 일치여부를 검사하여 파일 다운로드 제공 여부를 결정하는 코드를 추가한다.
    except HTTPException as e:
        raise e

    return StreamingResponse(
        iterate_file_chunk(file_path),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_id}"},
    )
