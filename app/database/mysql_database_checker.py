import os

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


def mysql_database_checker(host, user, password, db_name):
    base_url = f"mysql+pymysql://{user}:{password}@{host}"

    try:
        engine = create_engine(base_url)
        result = ""

        with engine.connect() as conn:
            result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'")).scalar()

        if result == db_name:
            engine = create_engine(f"{base_url}/{db_name}")

            with engine.connect() as conn:
                result = conn.execute(
                    text("SHOW TABLES LIKE 'alembic_version'")
                ).scalar()

            if result == "alembic_version":
                return db_name

        return ""
    except Exception:
        return "error"


host = os.getenv("RDBMS_HOST_NAME")
user = os.getenv("RDBMS_USERNAME")
password = os.getenv("RDBMS_PASSWORD")
db_name = os.getenv("RDBMS_DB_NAME")

result = mysql_database_checker(host, user, password, db_name)

print(result)
