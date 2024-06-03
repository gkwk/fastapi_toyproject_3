import os
import sys
import re

# 현재 경로
current_directory = os.path.dirname(os.path.abspath(__file__))

# 부모 경로
parent_directory = os.path.dirname(current_directory)

# app 경로
sibling_directory = os.path.join(parent_directory, "app")

if sibling_directory not in sys.path:
    sys.path.append(sibling_directory)


from sqlalchemy.sql.schema import (
    Column,
    ScalarElementColumnDefault,
    CallableColumnDefault,
)

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

    return "|" + "|".join(model_formatted_detail_list) + "|"


def create_models_table():
    string = ""
    for name, model in PythonInspect.getmembers(DBModels, PythonInspect.isclass):
        model: Base

        string += name + "\n"
        string += "NAME|TYPE|NULLABLE|DEFAULT|PRIMARY_KEY\n"
        string += "|---|---|---|---|---|\n"

        for column in model.__table__.columns:
            column: Column
            string += get_column_formatted_detail_string(column) + "\n"

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
