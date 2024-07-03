#!/bin/bash

ENV_FILE=./app/.env

if [ -f $ENV_FILE ]; then
    sudo mkdir -p volume/database volume/ai_model_store volume/staticfile volume/log/app volume/log/nginx volume/redis volume/alembic_migrations

    SOURCE_DIR="app/volume/staticfile"
    DEST_DIR="volume/staticfile"

    sudo cp -r "$SOURCE_DIR"/* "$DEST_DIR/"

    sudo docker-compose --env-file ./app/.env up --build 
else
    echo "env file not found"
    exit 1
fi