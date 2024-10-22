import pytest
import requests_mock
from requests import utils
from copyroles.alma import AlmaClient

almaClient = AlmaClient("TEST", "https://example.com")


def test_get_alma_environment():
    with requests_mock.Mocker(case_sensitive=True) as mocker:
        mocker.get("https://example.com/conf/general", json={'environment_type': 'test'})
        environment = almaClient.get_alma_environment()
        assert environment.lower() == "test"


def test_get_alma_user():
    primary_id = "test@example.com"
    quoted_id = utils.quote(primary_id)
    with requests_mock.Mocker(case_sensitive=True) as mocker:
        mocker.get(f"https://example.com/users/{quoted_id}", json={'user': 'test'})
        user = almaClient.get_alma_user(primary_id)
        assert user['user'] == 'test'


def test_update_roles():
    roles = {"role":"test"}
    user = {
        "primary_id": "test@example.com"
    }
    quoted_id = utils.quote(user["primary_id"])
    expected_payload = {"primary_id": "test@example.com", "user_role": {"role": "test"}}
    with requests_mock.Mocker(case_sensitive=True) as mocker:
        mocker.put(f"https://example.com/users/{quoted_id}")
        almaClient.update_alma_roles(roles, user)
        print(mocker.last_request.json())
        assert expected_payload == mocker.last_request.json()
