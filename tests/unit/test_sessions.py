"""_summary_
"""

import pytest

from api.app import get_app_database
from api.models import CreateUserValidator
from tests.unit import app  # pylint: disable=unused-import
from tests.unit import add_users, client  # pylint: disable=unused-import
from tests.unit.helpers import u_test_http_response

ENDPOINT = "/v1/sessions"


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {
                "username": "jimenalogo",
                "password": "secret",
            },
            {
                "status_code": 201,
                "body": {
                    "access_token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImppbWVuYWxvZ28iLCJleHAiOjE2NzE5ODg4NTV9.VL_SsLk0t4HIRR6sPiF_5ambvlpQ-xfoUgl5GMvc5-0erZFHIWYnnRnNi12UvY6lA9yTp1FCaOFWXJ8bX5LoOw",
                    "access_token_expires_ at": "2022-12-25T17:20:55",
                    "id": "6385248afe09c73d411fda0a",
                    "is_active": True,
                    "refresh_token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYzODUyNDhhZmUwOWM3M2Q0MTFmZGEwYSIsInVzZXJuYW1lIjoiamltZW5hbG9nbyIsImV4cCI6MTY3NDU3OTk1NX0.WQVKFCB46ZZWnNcNNBDikw-ExGQroIuMNJxQ1C0WNE0rBP0pClMvUpusbsJemzxV0Yu_EoUKopGkUTBCuP-unA",
                    "refresh_token_expires_ at": "2023-01-24T17:05:55",
                    "user": {
                        "_id": "6385248afe09c73d411fda0a",
                        "created_at": "2022-12-25T17:05:55",
                        "email": "jimenalogo@gmail.com",
                        "mobile": "+573046628057",
                        "name": "Jimena Lopez",
                        "username": "jimenalogo",
                    },
                },
            },
        ),
    ],
    ids=[
        "ok",
    ],
)
def test_new_user_session_ok(
    client, data, expected, add_users
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    u_test_http_response(client, ENDPOINT, data, expected)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            b"",
            {
                "status_code": 400,
                "body": {
                    "code": "empty-request",
                    "message": "request body must be a valid json",
                },
            },
        ),
        (
            b"test bytes",
            {
                "status_code": 400,
                "body": {
                    "code": "empty-request",
                    "message": "request body must be a valid json",
                },
            },
        ),
        (
            "test string",
            {
                "status_code": 400,
                "body": {
                    "code": "empty-request",
                    "message": "request body must be a valid json",
                },
            },
        ),
        (
            123,
            {
                "status_code": 400,
                "body": {
                    "code": "empty-request",
                    "message": "request body must be a valid json",
                },
            },
        ),
    ],
    ids=[
        "none_body",
        "no_json_body_bytes",
        "no_json_body_string",
        "no_json_body_int",
    ],
)
def test_new_user_session_error_request_body(
    client, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    u_test_http_response(client, ENDPOINT, data, expected)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {},
            {
                "status_code": 400,
                "body": [
                    {"field": "username", "message": "field required"},
                    {"field": "password", "message": "field required"},
                ],
            },
        ),
        (
            {
                "password": "secret",
            },
            {
                "status_code": 400,
                "body": [{"field": "username", "message": "field required"}],
            },
        ),
        (
            {
                "username": "jimenalogo",
            },
            {
                "status_code": 400,
                "body": [{"field": "password", "message": "field required"}],
            },
        ),
    ],
    ids=[
        "missing_all",
        "missing_username",
        "missing_password",
    ],
)
def test_new_user_session_error_missing_fields(
    client, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    u_test_http_response(client, ENDPOINT, data, expected)
