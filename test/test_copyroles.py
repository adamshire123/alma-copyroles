import pytest
import requests_mock
from copyroles.copyroles import get_alma_environment, get_alma_user, update_alma_roles
from requests import utils


def test_get_alma_environment():
    with requests_mock.Mocker(case_sensitive=True) as mocker:
        mocker.get("https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/general", json={'environment_type': 'test'})
        environment = get_alma_environment()
        assert environment.lower() == "test"


def test_get_alma_user():
    primary_id = "test@example.com"
    with requests_mock.Mocker(case_sensitive=True) as mocker:
        mocker.get(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/{utils.quote(primary_id)}", json={'user': 'test'})
        user = get_alma_user(primary_id)
        assert user['user'] == 'test'


def test_update_roles():
    roles = {"role":"test"}
    user = {
        "primary_id": "test@example.com"
    }
    expected_payload = {"primary_id": "test@example.com", "user_role": {"role": "test"}}
    with requests_mock.Mocker(case_sensitive=True) as mocker:
        mocker.put(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/{utils.quote(user["primary_id"])}")
        update_alma_roles(roles, user)
        print(mocker.last_request.json())
        assert expected_payload == mocker.last_request.json()
