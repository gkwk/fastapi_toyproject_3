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
- 차후 추가

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