from database.database import database_dependency
from service.board.logic_get_boards import logic_get_boards


def get_boards(data_base: database_dependency, user_role: str):
    filter_dict = {}

    if user_role != "ROLE_ADMIN":
        filter_dict["is_available"] = True

    # 차후 비공개 게시판 조회 기능 추가

    return logic_get_boards(data_base=data_base, filter_dict=filter_dict)
