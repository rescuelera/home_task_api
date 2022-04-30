import pytest
import requests
from jsonschema import validate


def test_get_image_random_breeds_ok():
    r: requests.Response = requests.get("https://dog.ceo/api/breeds/image/random")
    assert r.status_code == 200
    json_obj = r.json()
    assert isinstance(json_obj, dict)
    assert "message" in json_obj
    assert json_obj["status"] == "success"


response_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "message": {
            "type": "string"
        },
        "status": {
            "type":
                "string"
        }
    },
    "required": [
        "message",
        "status"
    ]
}


def test_get_image_random_breeds_schema_validate():
    r: requests.Response = requests.get("https://dog.ceo/api/breeds/image/random")
    assert r.status_code == 200
    json_obj = r.json()
    validate(json_obj, response_schema)


def test_get_list_all_breeds_ok():
    r: requests.Response = requests.get("https://dog.ceo/api/breeds/list/all")
    assert r.status_code == 200
    json_obj = r.json()
    assert isinstance(json_obj, dict)
    assert "message" in json_obj
    assert json_obj["status"] == "success"


def test_get_random_image_for_breed_ok():
    r_list_all: requests.Response = requests.get("https://dog.ceo/api/breeds/list/all")
    assert r_list_all.status_code == 200
    json_obj_list_all = r_list_all.json()

    first_breed = next(iter(json_obj_list_all["message"]))

    r: requests.Response = requests.get("https://dog.ceo/api/breed/{breed}/images/random".format(breed=first_breed))
    assert r.status_code == 200
    json_obj = r.json()
    assert "message" in json_obj
    assert json_obj["status"] == "success"


@pytest.mark.parametrize("breed", ["my_dog", 1, None])
def test_get_random_image_for_breed_negative(breed):
    r: requests.Response = requests.get("https://dog.ceo/api/breed/{breed}/images/random".format(breed=breed))
    assert r.status_code == 404
    json_obj = r.json()
    assert "message" in json_obj
    assert json_obj["status"] == "error"
    assert json_obj["code"] == 404


@pytest.mark.parametrize("method", ["put", "delete", "patch"])
def test_get_random_image_for_breed_wrong_methods(method):
    r_list_all: requests.Response = requests.get("https://dog.ceo/api/breeds/list/all")
    assert r_list_all.status_code == 200
    json_obj_list_all = r_list_all.json()

    first_breed = next(iter(json_obj_list_all["message"]))

    r: requests.Response = requests.request(method,
                                            "https://dog.ceo/api/breed/{breed}/images/random".format(breed=first_breed))
    assert r.status_code == 405
    json_obj = r.json()
    assert "message" in json_obj
    assert json_obj["status"] == "error"
    assert json_obj["code"] == 405
