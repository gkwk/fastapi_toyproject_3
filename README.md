# 프로젝트 목표
- `fastapi_toyproject_2`를 기반으로 가독성이 좋고 확장성있는 코드를 만든다.

# 기술 스택
- FastAPI
- Docker
- GitHub Actions

# 구현 목표
- 사용자 기능을 구현한다.
- 관리자 기능을 구현한다.
- 게시판 기능을 구현한다.
- WebSocket을 활용한 대화 기능을 구현한다.
- 비동기적인 AI 서빙을 구현한다.
- 로그 기능을 구현한다.
- 테스트 기능을 구현한다.
- MongoDB와 Redis 사용 함수를 구현한다.

# 구현 사항
- [ ] User
    - [ ] 회원가입
    - [ ] 로그인
    - [ ] 사용자 정보 보기
    - [ ] 사용자 정보 수정
    - [ ] 게시판 접근 권한 보기
    - [ ] 비밀번호 초기화 기능
    - [ ] JWT refresh token 기능
    - [ ] JWT access token 블랙리스트
- [ ] Admin
    - [ ] 터미널에서의 계정 생성
    - [ ] 사용자 리스트 보기
    - [ ] 사용자 게시판 접근 권한 수정
    - [ ] 사용자 차단
    - [ ] 게시판 추가
- [ ] Board
    - [ ] 추가 가능한 개별 게시판
    - [ ] 게시글 CRUD
    - [ ] 게시글 내 댓글 CRUD
    - [ ] 댓글 갯수 표시
    - [ ] 조회수 표시
    - [ ] 추천수 표시
    - [ ] 파일 첨부 기능
- [ ] Chat
    - [ ] WebSocket 기반 Chat
    - [ ] 대화 로그 DB 저장
- [ ] AI
    - [ ] 비동기 작동
    - [ ] 비동기 결과 반환 및 저장
- [ ] Log
- [ ] Test
- [ ] MongoDB
- [ ] Redis

# 구현 필요 사항 임시 기록
- Board 접근 여부 변경시 작동하는 User의 접근 권한 변경 코드를 작성한다.
    - is_visible이 True -> False시
        - Admin 및 요청된 User들에게 접근 권한 부여
    - is_visible이 False -> True시
        - 기존에 부여된 접근 권한을 DB에서 삭제
- Post, Comment, AI 삭제시 저장된 파일들을 삭제하는 코드를 작성한다.
- Post, Comment에 파일 첨부된 생성 요청시 Post와 Comment의 id 부여를 위한 commit 과정을 변경한다.
    - 파일 저장이 완전히 완료되지 않았지만 Post와 Comment가 보이는 문제를 해결해야 한다.
- Swagger 문서에서 엔드포인트들의 함수 명칭을 변경한다.

# 데이터베이스
- SQLAlchemy를 사용한다.
- SQLite와 MySQL을 선택할 수 있게 한다.

# 데이터베이스 테이블 구조
AI
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|id|INTEGER|False|None|True|False|None|
|name|VARCHAR(64)|False|None|False|False|True|
|description|VARCHAR(256)|False|None|False|False|None|
|create_date|DATETIME|False|datetime.now|False|False|None|
|update_date|DATETIME|True|None|False|False|None|
|finish_date|DATETIME|True|None|False|False|None|
|is_visible|BOOLEAN|False|False|False|False|None|
|is_available|BOOLEAN|False|False|False|False|None|
|celery_task_id|VARCHAR(64)|False|None|False|False|None|

AI Relationships
|NAME|RELATIONSHIP|
|---|---|
|ai_logs|1 : N|

AIlog
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|id|INTEGER|False|None|True|False|None|
|user_id|INTEGER|False|None|False|True|None|
|ai_id|INTEGER|False|None|False|True|None|
|description|VARCHAR(256)|False|None|False|False|None|
|result|VARCHAR(256)|False|None|False|False|None|
|create_date|DATETIME|False|datetime.now|False|False|None|
|update_date|DATETIME|True|None|False|False|None|
|finish_date|DATETIME|True|None|False|False|None|
|is_finished|BOOLEAN|False|False|False|False|None|
|celery_task_id|VARCHAR(64)|False|None|False|False|None|

AIlog Relationships
|NAME|RELATIONSHIP|
|---|---|
|user|N : 1|
|ai|N : 1|

Board
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|id|INTEGER|False|None|True|False|None|
|name|VARCHAR(128)|False|None|False|False|True|
|information|VARCHAR(512)|False|None|False|False|None|
|is_visible|BOOLEAN|False|False|False|False|None|
|is_available|BOOLEAN|False|False|False|False|None|

Board Relationships
|NAME|RELATIONSHIP|
|---|---|
|users|N : M|
|posts|1 : N|

Chat
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|id|INTEGER|False|None|True|False|None|
|user_id|INTEGER|False|None|False|True|None|
|chat_session_id|INTEGER|False|None|False|True|None|
|content|VARCHAR(256)|False|None|False|False|None|
|create_date|DATETIME|False|datetime.now|False|False|None|
|update_date|DATETIME|True|None|False|False|None|
|is_visible|BOOLEAN|False|True|False|False|None|

Chat Relationships
|NAME|RELATIONSHIP|
|---|---|
|user|N : 1|
|chat_session|N : 1|

ChatSession
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|id|INTEGER|False|None|True|False|None|
|user_create_id|INTEGER|False|None|False|True|None|
|name|VARCHAR(64)|False|None|False|False|None|
|information|VARCHAR(256)|False|None|False|False|None|
|create_date|DATETIME|False|datetime.now|False|False|None|
|update_date|DATETIME|True|None|False|False|None|
|is_visible|BOOLEAN|False|True|False|False|None|
|is_closed|BOOLEAN|False|False|False|False|None|

ChatSession Relationships
|NAME|RELATIONSHIP|
|---|---|
|user_create|N : 1|
|users_connect|N : M|
|chats|1 : N|

Comment
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|id|INTEGER|False|None|True|False|None|
|user_id|INTEGER|False|None|False|True|None|
|post_id|INTEGER|False|None|False|True|None|
|content|VARCHAR(256)|False|None|False|False|None|
|create_date|DATETIME|False|datetime.now|False|False|None|
|update_date|DATETIME|True|None|False|False|None|
|is_file_attached|BOOLEAN|False|False|False|False|None|
|is_visible|BOOLEAN|False|True|False|False|None|

Comment Relationships
|NAME|RELATIONSHIP|
|---|---|
|user|N : 1|
|post|N : 1|
|attached_files|1 : N|

CommentFile
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|comment_id|INTEGER|False|None|True|True|None|
|post_id|INTEGER|False|None|True|True|None|
|file_uuid_name|VARCHAR(383)|False|None|True|False|None|
|file_original_name|VARCHAR(1024)|False|None|False|False|None|
|file_path|VARCHAR(1024)|False|None|False|False|None|
|create_date|DATETIME|False|datetime.now|False|False|None|

CommentFile Relationships
|NAME|RELATIONSHIP|
|---|---|
|comment|N : 1|

JWTList
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|user_id|INTEGER|False|None|True|False|None|
|refresh_token_uuid|VARCHAR(36)|False|None|False|False|None|
|refresh_token_unix_timestamp|BIGINT|False|None|False|False|None|
|access_token_uuid|VARCHAR(36)|False|None|False|False|None|
|access_token_unix_timestamp|BIGINT|False|0|False|False|None|

JWTList Relationships
|NAME|RELATIONSHIP|
|---|---|

Post
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|id|INTEGER|False|None|True|False|None|
|user_id|INTEGER|False|None|False|True|None|
|board_id|INTEGER|False|None|False|True|None|
|name|VARCHAR(64)|False|None|False|False|None|
|content|VARCHAR(1024)|False|None|False|False|None|
|create_date|DATETIME|False|datetime.now|False|False|None|
|update_date|DATETIME|True|None|False|False|None|
|number_of_view|INTEGER|False|0|False|False|None|
|number_of_comment|INTEGER|False|0|False|False|None|
|is_file_attached|BOOLEAN|False|False|False|False|None|
|is_visible|BOOLEAN|False|True|False|False|None|

Post Relationships
|NAME|RELATIONSHIP|
|---|---|
|user|N : 1|
|board|N : 1|
|comments|1 : N|
|attached_files|1 : N|

PostFile
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|post_id|INTEGER|False|None|True|True|None|
|board_id|INTEGER|False|None|True|True|None|
|file_uuid_name|VARCHAR(383)|False|None|True|False|None|
|file_original_name|VARCHAR(1024)|False|None|False|False|None|
|file_path|VARCHAR(1024)|False|None|False|False|None|
|create_date|DATETIME|False|datetime.now|False|False|None|

PostFile Relationships
|NAME|RELATIONSHIP|
|---|---|
|post|N : 1|

User
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|id|INTEGER|False|None|True|False|None|
|name|VARCHAR(64)|False|None|False|False|True|
|email|VARCHAR(256)|False|None|False|False|True|
|password|VARCHAR(1024)|False|None|False|False|None|
|password_salt|VARCHAR(1024)|False|None|False|False|None|
|role|VARCHAR(1024)|False|None|False|False|None|
|join_date|DATETIME|False|datetime.now|False|False|None|
|update_date|DATETIME|True|None|False|False|None|
|is_banned|BOOLEAN|False|False|False|False|None|

User Relationships
|NAME|RELATIONSHIP|
|---|---|
|boards|N : M|
|posts|1 : N|
|comments|1 : N|
|ai_logs|1 : N|
|chat_sessions_create|1 : N|
|chat_sessions_connect|N : M|
|chats|1 : N|

UserChatSessionTable
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|user_id|INTEGER|False|None|True|True|None|
|chat_session_id|INTEGER|False|None|True|True|None|
|create_date|DATETIME|False|datetime.now|False|False|None|

UserChatSessionTable Relationships
|NAME|RELATIONSHIP|
|---|---|

UserPermissionTable
NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|
|---|---|---|---|---|---|---|
|user_id|INTEGER|False|None|True|True|None|
|board_id|INTEGER|False|None|True|True|None|
|create_date|DATETIME|False|datetime.now|False|False|None|

UserPermissionTable Relationships
|NAME|RELATIONSHIP|
|---|---|



# AI_test.csv
```math
y = 4x_0 + 5x_1 + 2x_2 + 7x_3 + 0.1x_4 + 15x_5 + 0.05x_6+ x_7
```

# 실행방법
- .env 파일 작성
- 터미널에서 아래의 명령어 입력
```bash
sudo bash project_init.sh
```

# 겪은 문제점들
- router의 순환 참조 오류
    > 기존 프로젝트는 router에 관련 함수들이 모두 포함되어 코드의 가독성이 저하되었다. 기능 별 파일의 단순 분리를 진행하였으나 순환 참조 오류가 발생하였다. 문제 해결을 위해 router 변수 정의 후, 모듈 불러오기를 시도했지만, import문의 분리로 인한 가독성 저하와 메모리 누수 등의 위험성을 고려하여, routing 데코레이터와 routing 함수를 분리하여 router.py에서 routing 데코레이터를 사용하는 방법을 적용하였다.
    `(ex : app\router\v1\main\router.py)`
- model의 순환 참조 오류
    > 기존에 models에 모두 포함시켰던 entity로 인해 코드의 가독성이 심각하게 저하되었다. 이를 해결하기 위해 entity 별 파일 분리가 필요하다고 느꼈다. entity들을 분리하고 `__init__.py`를 통한 모두 불러오기를 시행한 결과, entity간의 순환 참조 오류가 발생하였다. 이를 해결하기 위해 `typing` 모듈의 `TYPE_CHECKING`을 사용하였다.
- boards에서의 반환값 처리
    > 사용자의 `role`에 따라 반환받는 값의 변화가 있어야 한다고 생각하였다. `(ex: 일반 사용자가 봐서는 안되는 '서비스 사용 가능 여부'같은 정보들)` URL 통일성 유지와 코드의 복잡성을 줄이기 위해 `FastAPI`와 `pydantic`이 Access token의 `role`을 확인하고 router에 등록된 schema에 따라 자동으로 반환값을 변경하도록 하였다. `(ex: app\router\v1\boards\root\http_get.py)` SQL을 사용하는 것보다 성능이 좋지 않을 수 있지만, 성능상 문제가 발생하는 부분은 나중에 개별적으로 최적화하는 것이 더 낫다는 생각을 하였다.
- celery의 Task 타입 힌트 문제
    > `celery` 사용을 위해 관련 함수에 데코레이터를 붙여도 IDE가 데코레이터가 붙은 함수를 `Task` 타입으로 인식하지 못했다. 이를 해결하기 위해 `typing`의 `cast`를 사용하였다.
    `(ex: app\celery_app\v1\ais\tasks.py)`
- Form과 Pydantic의 유효성 검사 사용하기
    > 파일을 받고 처리하기 위해서 FastAPI의 `Form`을 사용하였다. 하지만 이런 접근으로는 Pydantic의 유효성 검사를 사용할 수 없으므로 `Form` 스키마에 `Pydantic` 스키마의 인스턴스를 생성하고 반환하는 class method를 추가하였다. 또한 의존성 주입 과정에서 유효성 검사를 통과하지 못할 경우 `HTTPException`을 발생시키도록 하여 사용자가 오류 원인을 알 수 있게 하였다.
    `(ex: app\schema\posts\request_post_detail_patch.py // app\router\v1\boards\id\posts\post_id\http_patch.py)`
- 웹소켓 인증 문제
    > 웹소켓은 공식적으로 `커스텀 헤더`를 추가할 수 없기에 사용자 인증 과정 선택에 어려움을 겪었다. 현재 프로젝트에 적용한 방법은 사용자 access token으로 `웹소켓 전용 access token`을 발행하고 쿼리 스트링으로 웹소켓 전용 access token을 받아 사용자 access token이 웹소켓 연결 과정에서 노출되는 위험을 최소화한 뒤, 연결된 웹소켓을 통해 사용자 access token을 지속적으로 받아 사용자가 검증되도록 하였다.
- Middleware 가독성 문제
    > `main.py`에 Middleware 관련 코드가 모두 포함될 경우 코드의 가독성이 저하가 예상되었다. 이를 해결하기 위해 `http_middleware`폴더를 추가한 뒤, Middleware 코드를 해당 폴더로 옮겼다. 코드 이전 이후, `main.py`에서 Middleware를 추가하는 코드만 유지하여 가독성을 향상시켰다.
- Board 접근 권한 문제
    > 현재 게시판 접근시 게시판의 공개여부`(is_visible)`에 따라 scope에 포함된 접근 권한을 검사하고 있다. 접근할 게시판의 `is_visible` 값을 검사하기 위해 DB를 조회하는 과정이 발생하고, 성능에 문제를 발생시킬 위험이 있다고 판단하였다. 문제 해결을 위해 메모리에 게시판들의 `is_visible` 값들을 캐싱하는 방법을 도입하였고, 라우터에서 캐싱된 게시판들의 `is_visible` 값들과 Access token에 저장된 scope를 비교하여 게시판 접근 권한을 검사하도록 하였다.

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
│       │   └── get_user_access_token_payload.py
│       ├── issue_user_jwt.py
│       ├── oauth2_scheme.py
│       ├── password_context.py
│       ├── refresh_token
│       │   ├── __init__.py
│       │   ├── decode_refresh_token.py
│       │   ├── delete_refresh_token.py
│       │   ├── generate_refresh_token.py
│       │   ├── get_refresh_token_from_cookie.py
│       │   └── get_user_refresh_token_payload.py
│       ├── reissue_access_token.py
│       ├── scope_checker.py
│       └── websocket_access_token
│           ├── __init__.py
│           ├── decode_websocket_access_token.py
│           ├── generate_websocket_access_token.py
│           ├── get_user_websocket_access_token_payload.py
│           └── get_websocket_access_token_from_query.py
├── celery_app
│   ├── __init__.py
│   ├── beat
│   │   └── .gitkeep
│   ├── celery.py
│   ├── tasks.py
│   └── v1
│       ├── __init__.py
│       ├── ailogs
│       │   ├── __init__.py
│       │   └── tasks.py
│       ├── ais
│       │   ├── __init__.py
│       │   └── tasks.py
│       └── posts
│           ├── __init__.py
│           └── tasks.py
├── config
│   ├── __init__.py
│   └── config.py
├── data_wrapper
│   ├── __init__.py
│   ├── access_token_payload.py
│   ├── refresh_token_payload.py
│   └── websocket_access_token_payload.py
├── database
│   ├── __init__.py
│   ├── alembic_template_mysql
│   │   ├── alembic.ini.mako
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic_template_sqlite
│   │   ├── alembic.ini.mako
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── cache.py
│   ├── database.py
│   ├── integrity_error_message_parser.py
│   ├── mysql_database_checker.py
│   └── sqlite_naming_convention.py
├── exception_message
│   ├── __init__.py
│   ├── http_exception_params.py
│   └── sql_exception_messages.py
├── http_middleware
│   ├── __init__.py
│   └── log_requests.py
├── lifespan
│   ├── __init__.py
│   └── lifespan.py
├── logger
│   ├── __init__.py
│   ├── custom_logger.py
│   ├── logger_methods.py
│   └── logger_setting.py
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
│   ├── post_view_increment.py
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
│       │   ├── board_id
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
│       │   ├── http_get.py
│       │   ├── http_post.py
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
│       │   ├── router.py
│       │   └── user_id
│       │       ├── __init__.py
│       │       ├── http_delete.py
│       │       ├── http_get.py
│       │       ├── http_patch.py
│       │       └── router.py
│       ├── v1_router.py
│       ├── v1_tags.py
│       └── v1_url.py
├── run.py
├── run_dev_local.py
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
├── service
│   ├── __init__.py
│   ├── ai
│   │   ├── __init__.py
│   │   ├── logic_create_ai.py
│   │   ├── logic_get_ai.py
│   │   ├── logic_get_ai_with_id.py
│   │   ├── logic_get_ais.py
│   │   └── router_logic
│   │       ├── __init__.py
│   │       ├── create_ai.py
│   │       ├── delete_ai.py
│   │       ├── get_ai_detail.py
│   │       ├── get_ais.py
│   │       └── update_ai.py
│   ├── ailog
│   │   ├── __init__.py
│   │   ├── logic_create_ailog.py
│   │   ├── logic_get_ailog.py
│   │   ├── logic_get_ailogs.py
│   │   └── router_logic
│   │       ├── __init__.py
│   │       ├── create_ailog.py
│   │       ├── delete_ailog.py
│   │       ├── get_ailog_detail.py
│   │       ├── get_ailogs.py
│   │       └── update_ailog.py
│   ├── auth
│   │   ├── __init__.py
│   │   └── router_logic
│   │       ├── __init__.py
│   │       ├── login.py
│   │       └── logout.py
│   ├── base_update_manager.py
│   ├── base_update_processor.py
│   ├── board
│   │   ├── __init__.py
│   │   ├── logic_get_board.py
│   │   ├── logic_get_boards.py
│   │   └── router_logic
│   │       ├── __init__.py
│   │       ├── create_board.py
│   │       ├── delete_board.py
│   │       ├── get_board_detail.py
│   │       ├── get_boards.py
│   │       └── update_board.py
│   ├── chat
│   │   ├── __init__.py
│   │   ├── logic_get_chat.py
│   │   ├── logic_get_chats.py
│   │   └── router_logic
│   │       ├── __init__.py
│   │       ├── delete_chat.py
│   │       ├── get_chat_detail.py
│   │       └── get_chats.py
│   ├── chat_session
│   │   ├── __init__.py
│   │   ├── logic_create_chat_session.py
│   │   ├── logic_get_chat_session.py
│   │   ├── logic_get_chat_sessions.py
│   │   └── router_logic
│   │       ├── __init__.py
│   │       ├── create_chat_session.py
│   │       ├── delete_chat_session.py
│   │       ├── get_chat_session_detail.py
│   │       ├── get_chat_sessions.py
│   │       └── update_chat_session.py
│   ├── comment
│   │   ├── __init__.py
│   │   ├── logic_create_comment.py
│   │   ├── logic_get_comment.py
│   │   ├── logic_get_comments.py
│   │   └── router_logic
│   │       ├── __init__.py
│   │       ├── create_comment.py
│   │       ├── delete_comment.py
│   │       ├── get_comment_detail.py
│   │       ├── get_comments.py
│   │       └── update_comment.py
│   ├── post
│   │   ├── __init__.py
│   │   ├── logic_create_post.py
│   │   ├── logic_get_post.py
│   │   ├── logic_get_posts.py
│   │   └── router_logic
│   │       ├── __init__.py
│   │       ├── create_post.py
│   │       ├── delete_post.py
│   │       ├── get_post_detail.py
│   │       ├── get_posts.py
│   │       └── update_post.py
│   └── user
│       ├── __init__.py
│       ├── logic_create_user.py
│       ├── logic_get_user.py
│       ├── logic_get_user_with_email.py
│       ├── logic_get_user_with_id.py
│       ├── logic_get_user_with_username.py
│       ├── logic_get_users.py
│       └── router_logic
│           ├── __init__.py
│           ├── create_user.py
│           ├── delete_user.py
│           ├── get_user_detail.py
│           ├── get_users.py
│           └── update_user.py
├── terminal_command
│   ├── __init__.py
│   └── create_super_user.py
├── test
│   ├── __init__.py
│   ├── conftest.py
│   ├── main_test
│   │   ├── __init__.py
│   │   ├── parameters
│   │   │   └── __init__.py
│   │   └── scripts.py
│   ├── pytest_test
│   │   ├── __init__.py
│   │   ├── parameters
│   │   │   └── __init__.py
│   │   └── scripts.py
│   └── test_run.py
└── volume
    ├── ai_model_store
    │   └── .gitkeep
    ├── database
    │   └── .gitkeep
    ├── log
    │   └── .gitkeep
    └── staticfile
        ├── .gitkeep
        └── AI_test.CSV
```