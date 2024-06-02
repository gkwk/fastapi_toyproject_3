# 프로젝트 목표
- `fastapi_toyproject_2`를 기반으로 가독성이 좋고 확장성있는 코드를 만든다.

# 사용 Tools
- FastAPI

# 구현 목표
- 차후 추가

# 구현 사항
- 차후 추가

# 데이터베이스
- SQLAlchemy를 사용한다.
- SQLite와 MySQL을 선택할 수 있게 한다.
- MongoDB와 Redis를 사용한다.

# 데이터베이스 테이블 구조
<!-- DB_TABLE_START -->
<!-- DB_TABLE_END -->

# AI_test.csv
```math
y = 4x_0 + 5x_1 + 2x_2 + 7x_3 + 0.1x_4 + 15x_5 + 0.05x_6+ x_7
```

# 실행방법(자동)
- .env 파일 작성
- 터미널에서 아래의 명령어 입력
```bash
sudo bash project_init.sh
```

# 실행방법(수동)
- .env 파일 작성
- 각각의 터미널에서 아래의 명령어들을 입력
```bash
app_init_local.sh
celery -A celery_app worker -l info --pool=solo
```

# 겪은 문제점들
- router의 순환 참조 오류
    > 기존에 router에 모두 포함시켰던 기능들로 인해 코드의 가독성이 심각하게 저하되었다. 이를 해결하기 위해 기능 별 파일 분리가 필요하다고 느꼈다. 기능들을 분리하고 모듈 불러오기를 각 파일들의 최상단에서 한번에 시행한 결과, router 순환 참조 오류가 발생하였다. 이를 해결하기 위해 router 변수 정의 후, 모듈 불러오기를 시행하였다.
    `(ex : app\router\v1\main\router.py)`
- model의 순환 참조 오류
    > 기존에 models에 모두 포함시켰던 entity로 인해 코드의 가독성이 심각하게 저하되었다. 이를 해결하기 위해 entity 별 파일 분리가 필요하다고 느꼈다. entity들을 분리하고 `__init__.py`를 통한 모두 불러오기를 시행한 결과, entity간의 순환 참조 오류가 발생하였다. 이를 해결하기 위해 `typing` 모듈의 `TYPE_CHECKING`을 사용하였다.
- boards에서의 반환값 처리
    > 사용자의 `role`에 따라 반환받는 값의 변화가 있어야 한다고 생각하였다. `(ex: 일반 사용자가 봐서는 안되는 '서비스 사용 가능 여부'같은 정보들)` URL 통일성 유지와 코드의 복잡성을 줄이기 위해 `FastAPI`와 `pydantic`이 Access token의 `role`을 확인하고 router에 등록된 schema에 따라 자동으로 반환값을 변경하도록 하였다. `(ex: app\router\v1\boards\root\http_get.py)` SQL을 사용하는 것보다 성능이 좋지 않을 수 있지만, 성능상 문제가 발생하는 부분은 나중에 개별적으로 최적화하는 것이 더 낫다는 생각을 하였다.
- celery의 Task 타입 힌트 문제
    > `celery` 사용을 위해 관련 함수에 데코레이터를 붙여도 IDE가 데코레이터가 붙은 함수를 `Task` 타입으로 인식하지 못했다. 이를 해결하기 위해 `typing`의 `cast`를 사용하였다.
    `(ex: app\celery_app\v1\ais\tasks.py)`
- Form과 Pydantic의 유효성 검사 사용하기
    > 파일을 받고 처리하기 위해서 FastAPI의 `Form`을 사용하였다. 하지만 이런 접근으로는 Pydantic의 유효성 검사를 사용할 수 없으므로 성능 손해를 감수하고 `Form` 스키마에 `Pydantic` 스키마의 인스턴스를 생성하는 과정을 추가하였다. 또한 의존성 주입 과정에서 유효성 검사를 통과하지 못할 경우 `HTTPException`을 발생시키도록 하여 사용자가 오류 원인을 알 수 있게 하였다.
    `(ex: app\router\v1\boards\id\posts\http_post.py)`
    > post의 patch 기능을 추가하던 중, 기존 `Form` 스키마에서 `Pydantic` 스키마로 변환하는 과정에서 요청하지 않은 필드가 포함되는 문제 등이 발생하였다. 이를 보완한 스키마를 post의 patch에 적용하였다.
    `(ex: app\schema\posts\request_post_detail_patch.py // app\router\v1\boards\id\posts\post_id\http_patch.py)`
- 웹소켓 인증 문제
    > 웹소켓은 공식적으로 `커스텀 헤더`를 추가할 수 없기에 사용자 인증 과정 선택에 어려움을 겪었다. 현재 프로젝트에 적용한 방법은 사용자 access token으로 `웹소켓 전용 access token`을 발행하고 쿼리 스트링으로 웹소켓 전용 access token을 받아 사용자 access token이 웹소켓 연결 과정에서 노출되는 위험을 최소화한 뒤, 연결된 웹소켓을 통해 사용자 access token을 지속적으로 받아 사용자가 검증되도록 하였다.

# 프로젝트 구조
```text
app
├── .env-example
├── app_init.sh
├── app_init_local.sh
├── auth
│   ├── __init__.py
│   └── jwt
│       ├── __init__.py
│       ├── access_token
│       │   ├── __init__.py
│       │   ├── ban_access_token.py
│       │   ├── decode_access_token.py
│       │   ├── generate_access_token.py
│       │   ├── get_access_token_from_header.py
│       │   ├── get_user_access_token_payload.py
│       │   ├── validate_after_access_token.py
│       │   └── validate_before_access_token.py
│       ├── issue_user_jwt.py
│       ├── oauth2_scheme.py
│       ├── password_context.py
│       ├── refresh_token
│       │   ├── __init__.py
│       │   ├── decode_refresh_token.py
│       │   ├── delete_refresh_token.py
│       │   ├── generate_refresh_token.py
│       │   ├── get_refresh_token_from_cookie.py
│       │   ├── get_user_refresh_token_payload.py
│       │   ├── validate_after_refresh_token.py
│       │   └── validate_before_refresh_token.py
│       ├── reissue_access_token.py
│       ├── scope_checker.py
│       ├── validate_before_issue_user_jwt.py
│       └── websocket_access_token
│           ├── __init__.py
│           ├── decode_websocket_access_token.py
│           ├── generate_websocket_access_token.py
│           ├── get_user_websocket_access_token_payload.py
│           ├── get_websocket_access_token_from_query.py
│           ├── validate_after_websocket_access_token.py
│           └── validate_before_websocket_access_token.py
├── celery_app
│   ├── __init__.py
│   ├── celery.py
│   ├── tasks.py
│   └── v1
│       ├── __init__.py
│       ├── ailogs
│       │   ├── __init__.py
│       │   └── tasks.py
│       └── ais
│           ├── __init__.py
│           └── tasks.py
├── config
│   ├── __init__.py
│   └── config.py
├── database
│   ├── __init__.py
│   ├── alembic_template_sqlite
│   │   ├── alembic.ini.mako
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── database.py
│   └── sqlite_naming_convention.py
├── exception_message
│   ├── __init__.py
│   └── http_exception_params.py
├── lifespan
│   ├── __init__.py
│   └── lifespan.py
├── main.py
├── models
│   ├── __init__.py
│   ├── ai.py
│   ├── ailog.py
│   ├── board.py
│   ├── chat.py
│   ├── chat_session.py
│   ├── comment.py
│   ├── comment_file.py
│   ├── jwt_access_token_blacklist.py
│   ├── jwt_list.py
│   ├── post.py
│   ├── post_file.py
│   ├── user.py
│   ├── user_board_table.py
│   └── user_chat_session_table.py
├── router
│   ├── __init__.py
│   └── v1
│       ├── __init__.py
│       ├── ais
│       │   ├── __init__.py
│       │   ├── ai_id
│       │   │   ├── __init__.py
│       │   │   ├── ailogs
│       │   │   │   ├── __init__.py
│       │   │   │   ├── ailog_id
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   ├── http_delete.py
│       │   │   │   │   ├── http_get.py
│       │   │   │   │   ├── http_patch.py
│       │   │   │   │   └── router.py
│       │   │   │   ├── http_get.py
│       │   │   │   ├── http_post.py
│       │   │   │   └── router.py
│       │   │   ├── http_delete.py
│       │   │   ├── http_get.py
│       │   │   ├── http_patch.py
│       │   │   └── router.py
│       │   ├── http_get.py
│       │   ├── http_post.py
│       │   └── router.py
│       ├── auth
│       │   ├── __init__.py
│       │   ├── issue_websocket_access_token
│       │   │   ├── __init__.py
│       │   │   ├── http_get.py
│       │   │   └── router.py
│       │   ├── login
│       │   │   ├── __init__.py
│       │   │   ├── http_post.py
│       │   │   └── router.py
│       │   ├── logout
│       │   │   ├── __init__.py
│       │   │   ├── http_post.py
│       │   │   └── router.py
│       │   ├── reissue_access_token
│       │   │   ├── __init__.py
│       │   │   ├── http_get.py
│       │   │   └── router.py
│       │   └── router.py
│       ├── boards
│       │   ├── __init__.py
│       │   ├── http_get.py
│       │   ├── http_post.py
│       │   ├── id
│       │   │   ├── __init__.py
│       │   │   ├── http_delete.py
│       │   │   ├── http_get.py
│       │   │   ├── http_patch.py
│       │   │   ├── posts
│       │   │   │   ├── __init__.py
│       │   │   │   ├── http_get.py
│       │   │   │   ├── http_post.py
│       │   │   │   ├── post_id
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   ├── comments
│       │   │   │   │   │   ├── __init__.py
│       │   │   │   │   │   ├── comment_id
│       │   │   │   │   │   │   ├── __init__.py
│       │   │   │   │   │   │   ├── http_delete.py
│       │   │   │   │   │   │   ├── http_get.py
│       │   │   │   │   │   │   ├── http_patch.py
│       │   │   │   │   │   │   └── router.py
│       │   │   │   │   │   ├── http_get.py
│       │   │   │   │   │   ├── http_post.py
│       │   │   │   │   │   └── router.py
│       │   │   │   │   ├── http_delete.py
│       │   │   │   │   ├── http_get.py
│       │   │   │   │   ├── http_patch.py
│       │   │   │   │   └── router.py
│       │   │   │   └── router.py
│       │   │   └── router.py
│       │   └── router.py
│       ├── chat_sessions
│       │   ├── __init__.py
│       │   ├── chat_session_id
│       │   │   ├── __init__.py
│       │   │   ├── chats
│       │   │   │   ├── __init__.py
│       │   │   │   ├── chat_id
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   ├── http_delete.py
│       │   │   │   │   ├── http_get.py
│       │   │   │   │   └── router.py
│       │   │   │   ├── http_get.py
│       │   │   │   └── router.py
│       │   │   ├── http_delete.py
│       │   │   ├── http_get.py
│       │   │   ├── http_patch.py
│       │   │   ├── router.py
│       │   │   └── ws
│       │   │       ├── __init__.py
│       │   │       ├── http_get.py
│       │   │       ├── router.py
│       │   │       └── websocket_chat_session.py
│       │   ├── http_get.py
│       │   ├── http_post.py
│       │   └── router.py
│       ├── main
│       │   ├── __init__.py
│       │   ├── http_get.py
│       │   └── router.py
│       ├── users
│       │   ├── __init__.py
│       │   ├── http_get.py
│       │   ├── http_post.py
│       │   ├── id
│       │   │   ├── __init__.py
│       │   │   ├── http_delete.py
│       │   │   ├── http_get.py
│       │   │   ├── http_patch.py
│       │   │   └── router.py
│       │   └── router.py
│       ├── v1_router.py
│       ├── v1_tags.py
│       └── v1_url.py
├── schema
│   ├── __init__.py
│   ├── ailogs
│   │   ├── __init__.py
│   │   ├── request_ailog_create.py
│   │   ├── request_ailog_detail_patch.py
│   │   ├── response_ailog_detail.py
│   │   └── response_ailogs.py
│   ├── ais
│   │   ├── __init__.py
│   │   ├── request_ai_create.py
│   │   ├── request_ai_detail_patch.py
│   │   ├── response_ai_detail.py
│   │   └── response_ais.py
│   ├── boards
│   │   ├── __init__.py
│   │   ├── request_board_create.py
│   │   ├── request_board_detail_patch.py
│   │   ├── response_board_detail.py
│   │   └── response_boards.py
│   ├── chat_sessions
│   │   ├── __init__.py
│   │   ├── request_chat_session_create.py
│   │   ├── request_chat_session_detail_patch.py
│   │   ├── response_chat_session_detail.py
│   │   └── response_chat_sessions.py
│   ├── chats
│   │   ├── __init__.py
│   │   ├── request_chat_create.py
│   │   ├── response_chat_detail.py
│   │   └── response_chats.py
│   ├── comments
│   │   ├── __init__.py
│   │   ├── request_comment_create.py
│   │   ├── request_comment_detail_patch.py
│   │   ├── response_comments.py
│   │   └── response_post_detail.py
│   ├── login
│   │   └── __init__.py
│   ├── posts
│   │   ├── __init__.py
│   │   ├── request_post_create.py
│   │   ├── request_post_detail_patch.py
│   │   ├── response_post_detail.py
│   │   └── response_posts.py
│   ├── terminal
│   │   ├── __init__.py
│   │   ├── admin_create_email.py
│   │   ├── admin_create_name.py
│   │   └── admin_create_password.py
│   └── users
│       ├── __init__.py
│       ├── request_user_detail_patch.py
│       ├── request_user_join.py
│       ├── response_user_detail.py
│       └── response_users.py
├── terminal_command
│   ├── __init__.py
│   └── create_super_user.py
└── volume
    ├── ai_model_store
    │   └── .keep
    ├── database
    │   └── .keep
    └── staticfile
        ├── .keep
        └── AI_test.CSV
```