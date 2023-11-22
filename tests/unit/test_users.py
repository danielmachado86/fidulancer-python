"""_summary_
"""

import pytest

from tests import FAKE_OID, FAKE_TIME
from tests.unit import app  # pylint: disable=unused-import
from tests.unit import client  # pylint: disable=unused-import
from tests.unit.helpers import u_test_post_response

TEST_ENDPOINT = "/v1/users"


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
                "password": "secret",
            },
            {
                "status_code": 201,
                "body": {
                    "_id": str(FAKE_OID),
                    "name": "Jimena Lopez",
                    "username": "jimenalogo",
                    "email": "jimenalogo@gmail.com",
                    "mobile": "+573046628057",
                    "created_at": FAKE_TIME.isoformat(),
                },
            },
        ),
    ],
    ids=[
        "ok",
    ],
)
def test_user_registration_ok(
    client, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    u_test_post_response(client, TEST_ENDPOINT, data, expected)


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
def test_user_registration_error_request_body(
    client, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    u_test_post_response(client, TEST_ENDPOINT, data, expected)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {},
            {
                "status_code": 400,
                "body": [
                    {"field": "name", "message": "field required"},
                    {"field": "username", "message": "field required"},
                    {"field": "email", "message": "field required"},
                    {"field": "mobile", "message": "field required"},
                    {"field": "password", "message": "field required"},
                ],
            },
        ),
        (
            {
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
                "password": "secret",
            },
            {
                "status_code": 400,
                "body": [{"field": "name", "message": "field required"}],
            },
        ),
        (
            {
                "name": "Jimena Lopez",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
                "password": "secret",
            },
            {
                "status_code": 400,
                "body": [{"field": "username", "message": "field required"}],
            },
        ),
        (
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "mobile": "+573046628057",
                "password": "secret",
            },
            {
                "status_code": 400,
                "body": [{"field": "email", "message": "field required"}],
            },
        ),
        (
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "password": "secret",
            },
            {
                "status_code": 400,
                "body": [{"field": "mobile", "message": "field required"}],
            },
        ),
        (
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
            },
            {
                "status_code": 400,
                "body": [{"field": "password", "message": "field required"}],
            },
        ),
    ],
    ids=[
        "missing_all",
        "missing_name",
        "missing_username",
        "missing_email",
        "missing_mobile",
        "missing_password",
    ],
)
def test_user_registration_error_missing_fields(
    client, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    u_test_post_response(client, TEST_ENDPOINT, data, expected)
