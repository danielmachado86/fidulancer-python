"""_summary_
"""

from unittest.mock import patch

import pytest

from tests import FAKE_OID, FAKE_TIME  # pylint: disable=unused-import
from tests.unit import app  # pylint: disable=unused-import
from tests.unit import add_users, client
from tests.unit.helpers import u_test_http_response

TEST_ENDPOINT = "/v1/contracts"
TEST_USERNAME = "jimenalogo"


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {"name": "Contrato 1", "type": "rental"},
            {
                "status_code": 201,
                "body": {
                    "_id": str(FAKE_OID),
                    "name": "Contrato 1",
                    "type": "rental",
                    "created_at": FAKE_TIME.isoformat(),
                    "users": [
                        {"username": TEST_USERNAME, "added_at": FAKE_TIME.isoformat()}
                    ],
                },
            },
        ),
    ],
    ids=[
        "ok",
    ],
)
def test_create_contract_ok(
    client, data, expected, add_users
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    # we say that jwt_decode_handler will return {'user_id': '1'}
    with patch("api.auth.jwt.decode", return_value={"username": TEST_USERNAME}):
        headers = {"Authorization": "bearer test_token"}
        # as you can see current_identity['user_id'] is '1' (so, it was mocked in view)
        u_test_http_response(client, TEST_ENDPOINT, data, expected, headers=headers)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            [
                {"name": "contract_duration", "value": 12, "units": "months"},
                {"name": "star_date", "value": "15-05-2023", "units": "date"},
                {"name": "notice_period", "value": 3, "units": "months"},
            ],
            {
                "status_code": 201,
                "body": {
                    "_id": str(FAKE_OID),
                    "name": "Contrato 1",
                    "type": "rental",
                    "created_at": FAKE_TIME.isoformat(),
                    "users": [
                        {"username": TEST_USERNAME, "added_at": FAKE_TIME.isoformat()}
                    ],
                },
            },
        ),
    ],
    ids=[
        "ok",
    ],
)
def test_contract_add_parameters_ok(
    client, data, expected, add_users
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    # we say that jwt_decode_handler will return {'user_id': '1'}
    with patch("api.auth.jwt.decode", return_value={"username": TEST_USERNAME}):
        headers = {"Authorization": "bearer test_token"}
        # as you can see current_identity['user_id'] is '1' (so, it was mocked in view)
        u_test_http_response(client, TEST_ENDPOINT, data, expected, headers=headers)
