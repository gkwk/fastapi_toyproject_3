import os
import sys
from pathlib import Path
import re

# 현재 경로
current_directory = os.path.dirname(os.path.abspath(__file__))

# 부모 경로
parent_directory = os.path.dirname(current_directory)

# app 경로
sibling_directory = os.path.join(parent_directory, "app")

if sibling_directory not in sys.path:
    sys.path.append(sibling_directory)

from sqlalchemy import inspect
from sqlalchemy.orm import Mapper
from sqlalchemy.sql.schema import (
    Column,
    ScalarElementColumnDefault,
    CallableColumnDefault,
)

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from database.database import Base
import models as DBModels
import inspect as PythonInspect


def get_column_formatted_detail_string(column: Column):
    model_formatted_detail_list = []

    model_formatted_detail_list.append(str(column.name))
    model_formatted_detail_list.append(str(column.type))
    model_formatted_detail_list.append(str(column.nullable))

    if type(column.default) == ScalarElementColumnDefault:
        model_formatted_detail_list.append(str(column.default.arg))
    elif type(column.default) == CallableColumnDefault:
        if hasattr(column.default.arg, "__qualname__"):
            model_formatted_detail_list.append(str(column.default.arg.__qualname__))
        elif hasattr(column.default.arg, "__name__"):
            model_formatted_detail_list.append(str(column.default.arg.__name__))
        else:
            model_formatted_detail_list.append(str(column.default))
    else:
        model_formatted_detail_list.append(str(column.default))
    model_formatted_detail_list.append(str(column.primary_key))
    model_formatted_detail_list.append(str(len(column.foreign_keys) > 0))
    model_formatted_detail_list.append(str(column.unique))

    return "|" + "|".join(model_formatted_detail_list) + "|"


def create_models_table():
    string = ""
    for name, model in PythonInspect.getmembers(DBModels, PythonInspect.isclass):
        model: Base

        string += name + "\n"
        string += "NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY|FOREIGN_KEY|UNIQUE|\n"
        string += "|---|---|---|---|---|---|---|\n"

        for column in model.__table__.columns:
            column: Column
            string += get_column_formatted_detail_string(column) + "\n"

        string += "\n"

        string += name + " Relationships\n"
        string += "|NAME|RELATIONSHIP|\n"
        string += "|---|---|\n"

        inspector: Mapper = inspect(model)
        relationships = inspector.relationships
        for relationship in relationships:
            if relationship.secondary is not None:
                string += "|" + relationship.key + "|N : M|\n"
            elif relationship.uselist:
                string += "|" + relationship.key + "|1 : N|\n"
            else:
                related_model = relationship.mapper.entity
                related_model_inspector: Mapper = inspect(related_model)

                checker = False

                for related_model_relationship in related_model_inspector.relationships:
                    if (
                        related_model_relationship.mapper.entity == model
                        and related_model_relationship.uselist
                    ):
                        checker = True
                        break

                if checker:
                    string += "|" + relationship.key + "|N : 1|\n"
                else:
                    string += "|" + relationship.key + "|1 : 1|\n"

        string += "\n"

    return string


def get_updated_readme(readme_path, replace_string, regex_pattern=None):
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()

    if regex_pattern is None:
        regex_pattern = r"(<!-- DB_TABLE_START -->)(.*?)(<!-- DB_TABLE_END -->)"

    updated_content = re.sub(regex_pattern, replace_string, content, flags=re.DOTALL)

    return updated_content


if __name__ == "__main__":
    models_table = create_models_table()
    updated_readme = get_updated_readme("../README.md", models_table)
    with open("../README.md", "w", encoding="utf-8") as file:
        file.write(updated_readme)
