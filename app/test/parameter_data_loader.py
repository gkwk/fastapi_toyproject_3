import pytest
import orjson


def parameter_data_loader(path):
    test_data = {"argnames": None, "argvalues": []}

    with open(path, "r", encoding="UTF-8") as file:
        json_data: dict = orjson.loads(file.read())

    test_data["argnames"] = "pn," + json_data.get("argnames")

    for value in json_data.get("argvalues_pass", []):
        test_data["argvalues"].append(tuple([1, *value]))

    for value in json_data.get("argvalues_fail", []):
        value_temp = pytest.param(
            0, *value[:-1], marks=pytest.mark.xfail(reason=value[-1])
        )
        test_data["argvalues"].append(value_temp)

    return test_data
