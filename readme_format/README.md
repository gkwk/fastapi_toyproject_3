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
- User
    - [x] 회원가입
    - [x] 로그인
    - [x] 사용자 정보 보기
    - [x] 사용자 정보 수정
    - [x] 게시판 접근 권한
    - [x] 비밀번호 초기화 기능 (SMTP)
    - [x] JWT refresh token 기능
    - [x] JWT access token 블랙리스트
- Admin
    - [x] 터미널에서의 계정 생성
    - [x] 사용자 리스트 보기
    - [x] 사용자 게시판 접근 권한 수정
    - [ ] 사용자 차단
    - [x] 게시판 추가
- Board
    - [x] 추가 가능한 개별 게시판
    - [x] 게시글 CRUD
    - [x] 게시글 내 댓글 CRUD
    - [x] 조회수 표시
    - [x] 파일 첨부 기능
- Chat
    - [x] WebSocket 기반 Chat
    - [x] 대화 로그 DB 저장
- AI
    - [x] 비동기 작동
    - [x] 비동기 결과 반환 및 저장
- [x] Log
- [ ] Test
- [x] MongoDB
- [x] Redis

# 구현 필요 사항 임시 기록
- Board 접근 여부 변경시 작동하는 User의 접근 권한 변경 코드를 작성한다.
    - is_visible이 True -> False시
        - Admin 및 요청된 User들에게 접근 권한 부여
    - is_visible이 False -> True시
        - 기존에 부여된 접근 권한을 DB에서 삭제
- Post, Comment, AI 삭제시 저장된 파일들을 삭제하는 코드를 작성한다.
- Post, Comment에 파일 첨부된 생성 요청시 Post와 Comment의 id 부여를 위한 commit 과정을 변경한다.
    - 파일 저장이 완전히 완료되지 않았지만 Post와 Comment가 보이는 문제를 해결해야 한다.
- AI 파일 저장 방식의 변경 고려
    - 현재 AI 파일의 이름이 update로 인한 name 변경을 반영하지 못하는 문제가 있다. 이를 해결하기 위해, id와 uuid로 파일의 이름을 구성하는 방법 등의 도입을 고려해야 한다.

# 데이터베이스
- SQLAlchemy를 사용한다.
- SQLite와 MySQL을 선택할 수 있게 한다.

# 데이터베이스 테이블 구조
<!-- DB_TABLE_START -->
<!-- DB_TABLE_END -->

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

# PyTest 실행방법
```bash
pytest test/test_run.py
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
<!-- PROJECT_DIR_TREE_START -->
<!-- PROJECT_DIR_TREE_END -->
```