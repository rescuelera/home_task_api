import requests


def test_url_code(url_from_console, status_code_from_console):
    r: requests.Response = requests.get(url_from_console)
    assert r.status_code == status_code_from_console
