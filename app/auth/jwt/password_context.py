from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])


def get_password_context():
    return password_context
