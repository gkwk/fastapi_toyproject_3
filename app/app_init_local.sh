#!/bin/bash

ENV_FILE="./.env"

if [ -f $ENV_FILE ]; then
    source $ENV_FILE
else
    echo "env file not found"
    exit 1
fi

SQLITE_DB_FILE="./volume/database/${RDBMS_DB_NAME}.sqlite"
if [ "$RDBMS_DRIVER" = "mysql" ]; then
    ALEMBIC_TEMPLATE_FOLDER="./database/alembic_template_mysql"
else
    ALEMBIC_TEMPLATE_FOLDER="./database/alembic_template_sqlite"
fi
ALEMBIC_TEMPLATE_FOLDER_ABSOLUTE_PATH=$(realpath "$ALEMBIC_TEMPLATE_FOLDER")

if [ "$RDBMS_DRIVER" = "mysql" ]; then
    DB_USER=${!RDBMS_USERNAME_ENV:-$RDBMS_USERNAME_ENV}
    DB_PASS=${!RDBMS_PASSWORD_ENV:-$RDBMS_PASSWORD_ENV}

    RESULT=$(mysql -h "$RDBMS_HOST_NAME" -u "$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES LIKE '$RDBMS_DB_NAME';" | grep "$RDBMS_DB_NAME")

    if [ "$RESULT" == "$RDBMS_DB_NAME" ]; then
        :
    else
        alembic init -t "$ALEMBIC_TEMPLATE_FOLDER_ABSOLUTE_PATH" alembic_migrations
        alembic revision --autogenerate
        alembic upgrade head
    fi
# sqlite
else
    if [ -f $SQLITE_DB_FILE ]; then
        :
    else
        alembic init -t "$ALEMBIC_TEMPLATE_FOLDER_ABSOLUTE_PATH" alembic_migrations
        alembic revision --autogenerate
        alembic upgrade head
    fi
fi

python run_dev_local.py