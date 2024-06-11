#!/bin/bash

ENV_FILE=./.env
DB_FILE=./volume/database/test.sqlite
ALEMBIC_TEMPLATE_FOLDER=./database/alembic_template_sqlite
ALEMBIC_TEMPLATE_FOLDER_ABSOLUTE_PATH=$(realpath "$ALEMBIC_TEMPLATE_FOLDER")


if !([ -e $ENV_FILE ]); then
    echo "env file not found"
    exit 1
fi

if [ -e $DB_FILE ]; then
	python run.py
else
    alembic init -t "$ALEMBIC_TEMPLATE_FOLDER_ABSOLUTE_PATH" alembic_migrations
    alembic revision --autogenerate
    alembic upgrade head
    python main.py
fi