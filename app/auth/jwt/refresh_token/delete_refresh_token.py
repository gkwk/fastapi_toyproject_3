from models import JWTList
from database.database import database_dependency
from auth.jwt.access_token.ban_access_token import ban_access_token


def delete_refresh_token(
    data_base: database_dependency,
    user_id: int,
):
    user_jwt_information = data_base.query(JWTList).filter_by(user_id=user_id).first()
    if user_jwt_information:
        ban_access_token(data_base=data_base, user_id=user_id)
        data_base.delete(user_jwt_information)
        data_base.commit()

    # token ban 과정에서 비동기적으로 추가 ban 과정이 진행될 수 있으므로, 이를 위한 예외처리를 추가한다.