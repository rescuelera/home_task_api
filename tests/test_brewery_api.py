import pytest
import requests
from jsonschema import validate


@pytest.mark.xfail(reason="Bug in search functionality", strict=True)
@pytest.mark.parametrize("query", ["dog", "cat", "pig"])
def test_search_breveries_ok(query):
    r: requests.Response = requests.get(
        "https://api.openbrewerydb.org/breweries/search?query={query}".format(query=query))
    assert r.status_code == 200
    json_list = r.json()
    assert isinstance(json_list, list)
    for item in json_list:
        assert query in item["name"].lower()


@pytest.mark.parametrize("query", ["dog", "cat", "pig"])
def test_search_autocomplete_ok(query):
    r: requests.Response = requests.get(
        "https://api.openbrewerydb.org/breweries/autocomplete?query={query}".format(query=query))
    assert r.status_code == 200
    json_list = r.json()
    assert isinstance(json_list, list)
    for item in json_list:
        assert query in item["name"].lower()


response_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "properties": {
        "id": {
            "type": "string"
        },
        "name": {
            "type": "string"
        },
    },
    "required": [
        "id",
        "name",
    ],
}


def test_get_autocomplete_schema_validate():
    r: requests.Response = requests.get("https://api.openbrewerydb.org/breweries/autocomplete?query=dog")
    json_obj = r.json()
    validate(json_obj, response_schema)


def test_list_breveries_ok():
    r: requests.Response = requests.get("https://api.openbrewerydb.org/breweries")
    assert r.status_code == 200
    json_list = r.json()
    assert isinstance(json_list, list)


def test_get_brevery_ok():
    brevery_response = requests.get("https://api.openbrewerydb.org/breweries")
    json_list = brevery_response.json()
    brevery = json_list[0]["id"]
    r: requests.Response = requests.get("https://api.openbrewerydb.org/breweries/{brevery}".format(brevery=brevery))
    assert r.status_code == 200
    json_obj = r.json()
    assert isinstance(json_obj, dict)
