#!/bin/bash


SQLITE_DB_FILE="./volume/database/${RDBMS_DB_NAME}.sqlite"
if [ "$RDBMS_DRIVER" = "mysql" ]; then
    ALEMBIC_TEMPLATE_FOLDER="./database/alembic_template_mysql"
else
    ALEMBIC_TEMPLATE_FOLDER="./database/alembic_template_sqlite"
fi
ALEMBIC_TEMPLATE_FOLDER_ABSOLUTE_PATH=$(realpath "$ALEMBIC_TEMPLATE_FOLDER")

if [ "$RDBMS_DRIVER" = "mysql" ]; then
    RESULT=$(python database/mysql_database_checker.py)

    echo $RESULT

    if [ "$RESULT" == "$RDBMS_DB_NAME" ]; then
        :
    else
        alembic init -t "$ALEMBIC_TEMPLATE_FOLDER_ABSOLUTE_PATH" alembic_migrations

        mv alembic.ini ./alembic_migrations/

        alembic -c ./alembic_migrations/alembic.ini revision --autogenerate
        alembic -c ./alembic_migrations/alembic.ini upgrade head
    fi
# sqlite
else
    if [ -f $SQLITE_DB_FILE ]; then
        :
    else
        alembic init -t "$ALEMBIC_TEMPLATE_FOLDER_ABSOLUTE_PATH" alembic_migrations

        mv alembic.ini ./alembic_migrations/

        alembic -c ./alembic_migrations/alembic.ini revision --autogenerate
        alembic -c ./alembic_migrations/alembic.ini upgrade head
    fi
fi

python run_dev_local.py