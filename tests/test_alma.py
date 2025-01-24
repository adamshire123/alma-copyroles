from urllib.parse import quote

import pytest
import requests_mock

from copyroles.alma import AlmaClient


def test_alma_client_initialization():
    api_key = "test_api_key"
    base_url = "https://example.com/almaws/v1/"
    client = AlmaClient(api_key, base_url)

    assert client.api_key == api_key
    assert client.base_url == base_url
    assert client.headers["Authorization"] == f"apikey {api_key}"
    assert client.headers["Accept"] == "application/json"
    assert client.headers["Content-Type"] == "application/json"


def test_alma_client_default_base_url():
    api_key = "test_api_key"
    client = AlmaClient(api_key)

    assert client.api_key == api_key
    assert client.base_url == "https://api-na.hosted.exlibrisgroup.com/almaws/v1/"
    assert client.headers["Authorization"] == f"apikey {api_key}"
    assert client.headers["Accept"] == "application/json"
    assert client.headers["Content-Type"] == "application/json"


def test_get_alma_user():
    api_key = "test_api_key"
    client = AlmaClient(api_key)
    primary_id = "kerb@mit.edu"
    user_data = {"primary_id": primary_id, "user_role": [{"role": "test"}]}
    with requests_mock.Mocker() as m:
        m.get(f"{client.base_url}users/{quote(primary_id)}", json=user_data)
        response = client.get_alma_user(primary_id)
        assert response == user_data


def test_update_alma_roles():
    api_key = "test_api_key"
    client = AlmaClient(api_key)
    primary_id = "kerb@mit.edu"
    new_roles = [{"role": "test"}]
    user_to_update = {"primary_id": primary_id}
    quoted_id = quote(primary_id)
    expected_payload = {"primary_id": primary_id, "user_role": new_roles}
    with requests_mock.Mocker() as m:
        m.put(f"{client.base_url}users/{quoted_id}")
        client.update_alma_roles(new_roles, user_to_update)
        assert m.last_request.json() == expected_payload


def test_create_alma_user(user_record):
    api_key = "test_api_key"
    client = AlmaClient(api_key)
    with requests_mock.Mocker() as m:
        m.post(f"{client.base_url}users/")
        client.create_alma_user(user_record)
        assert m.last_request.json() == user_record


def test_alma_environment():
    api_key = "test_api_key"
    client = AlmaClient(api_key)
    environment_data = {"environment_type": "production"}
    with requests_mock.Mocker() as m:
        m.get(f"{client.base_url}conf/general", json=environment_data)
        environment = client.alma_environment
        assert environment == "production"


@pytest.fixture
def user_record():
    return {
        "link": "",
        "record_type": {"value": "STAFF"},
        "primary_id": "johns",
        "first_name": "John",
        "middle_name": "W",
        "last_name": "Smith",
        "pin_number": "4554",
        "user_title": {"value": ""},
        "job_category": {"value": "Cataloger"},
        "job_description": "The best cataloger",
        "gender": {"value": "MALE"},
        "user_group": {"value": "FACULTY"},
        "campus_code": {"value": "Main"},
        "web_site_url": "",
        "cataloger_level": {"value": ""},
        "preferred_language": {"value": "en"},
        "birth_date": "1979-01-11Z",
        "expiry_date": "2030-01-16Z",
        "purge_date": "2024-05-30Z",
        "account_type": {"value": "INTERNAL"},
        "external_id": "",
        "password": "12345",
        "force_password_change": "TRUE",
        "status": {"value": "ACTIVE"},
        "contact_info": {
            "address": [
                {
                    "preferred": "true",
                    "segment_type": "Internal",
                    "line1": "3598 N. Buckingham Road",
                    "line2": "",
                    "line3": "",
                    "line4": "",
                    "line5": "",
                    "city": "Scottsdale",
                    "state_province": "AZ",
                    "postal_code": "85054",
                    "country": {"value": "USA"},
                    "address_note": "",
                    "start_date": "2024-05-30Z",
                    "end_date": "2024-05-30Z",
                    "address_type": [{"value": "home"}],
                }
            ],
            "email": [
                {
                    "preferred": "true",
                    "segment_type": "Internal",
                    "email_address": "johns@mylib.org",
                    "description": "",
                    "email_type": [{"value": "personal"}],
                }
            ],
            "phone": [
                {
                    "preferred": "false",
                    "preferred_sms": "false",
                    "segment_type": "Internal",
                    "phone_number": "18005882300",
                    "phone_type": [{"value": "home"}],
                }
            ],
        },
        "user_identifier": [
            {
                "segment_type": "Internal",
                "id_type": {"value": "UNIV_ID"},
                "value": "johns691",
                "note": "",
                "status": "",
            }
        ],
        "user_role": [
            {
                "status": {"value": "NEW"},
                "scope": {"value": ""},
                "role_type": {"value": "200"},
                "expiry_date": "2024-05-30Z",
                "parameter": [
                    {
                        "type": {"value": ""},
                        "scope": {"value": ""},
                        "value": {"value": "CircDeskOp"},
                    }
                ],
            }
        ],
        "user_block": [
            {
                "segment_type": "Internal",
                "block_type": {"value": "LOAN"},
                "block_description": {"value": "CONSORTIA"},
                "block_status": "",
                "block_note": "",
                "created_by": "",
                "created_date": "2024-05-30T09:30:10Z",
                "expiry_date": "2019-12-18T14:36:48.659Z",
                "block_owner": "LIB2",
            }
        ],
        "user_note": [
            {
                "segment_type": "External",
                "note_type": {"value": "ERP"},
                "note_text": "ERP user note example",
                "user_viewable": "false",
                "popup_note": "false",
                "created_by": "",
                "created_date": "2024-05-30T09:30:10Z",
                "note_owner": "LIB1",
            }
        ],
        "user_statistic": [
            {
                "segment_type": "External",
                "statistic_category": {"value": "LOCAL"},
                "category_type": {"value": "COLLEGE"},
                "statistic_owner": "LIB2",
                "statistic_note": "",
            }
        ],
        "proxy_for_user": [{"link": "", "proxy_type": "RESEARCH"}],
        "rs_library": [{"code": {"value": ""}}],
        "library_notice": [
            {"code": {"value": "FulUserBorrowingActivityLetter"}, "value": "false"}
        ],
        "pref_first_name": "John",
        "pref_middle_name": "W",
        "pref_last_name": "Smith",
        "pref_name_suffix": "Junior",
        "is_researcher": "false",
        "researcher": {
            "researcher_first_name": "John",
            "researcher_middle_name": "W",
            "researcher_last_name": "Smith",
            "researcher_suffix": "Junior",
            "researcher_title": {"value": "PROF"},
            "profile_image_url": "",
            "photo_url": "",
            "profile_identifier_url": "",
            "display_title": "",
            "update_ORCID_profile": "false",
            "user_identifiers": [
                {
                    "segment_type": "Internal",
                    "id_type": {"value": "UNIV_ID"},
                    "value": "johns691",
                    "note": "",
                    "status": "",
                }
            ],
        },
    }
