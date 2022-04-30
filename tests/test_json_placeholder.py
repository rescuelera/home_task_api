import pytest
import requests
from jsonschema import validate


@pytest.mark.parametrize("postId", [1, 2, 3])
def test_get_comments_ok(postId):
    r: requests.Response = requests.get(
        "https://jsonplaceholder.typicode.com/comments?postId={postId}".format(postId=postId))
    assert r.status_code == 200
    json_list = r.json()
    assert isinstance(json_list, list)


def test_get_posts_ok():
    r: requests.Response = requests.get("https://jsonplaceholder.typicode.com/posts")
    assert r.status_code == 200
    json_list = r.json()
    assert isinstance(json_list, list)
    assert len(json_list) == 100


@pytest.mark.parametrize("post_number", [1, 2, 3])
def test_get_posts_post_number_ok(post_number):
    r: requests.Response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/{post_number}".format(post_number=post_number))
    assert r.status_code == 200
    json_obj = r.json()
    assert isinstance(json_obj, dict)


@pytest.mark.parametrize("post_number", [-1, "a", None])
def test_get_posts_post_number_negative(post_number):
    r: requests.Response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/{post_number}".format(post_number=post_number))
    assert r.status_code == 404
    json_obj = r.json()
    assert isinstance(json_obj, dict)


@pytest.mark.parametrize("post_number", [1, 2, 3])
def test_get_posts_post_number_comments_ok(post_number):
    r: requests.Response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/{post_number}/comments".format(post_number=post_number))
    assert r.status_code == 200
    json_list = r.json()
    assert isinstance(json_list, list)


response_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "properties": {
        "userId": {
            "type": "integer"
        },
        "id": {
            "type": "integer"
        },
        "title": {
            "type": "string"
        },
        "body": {
            "type": "string"
        }
    },
    "required": [
        "userId",
        "id",
        "title",
        "body",
    ]
}


def test_get_post_schema_validate():
    r: requests.Response = requests.get("https://jsonplaceholder.typicode.com/posts")
    json_obj = r.json()
    validate(json_obj, response_schema)
