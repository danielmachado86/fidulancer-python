"""_summary_
"""

from unittest.mock import patch

import pytest

from tests import FAKE_OID, FAKE_TIME  # pylint: disable=unused-import
from tests.unit import app  # pylint: disable=unused-import
from tests.unit import add_users, client
from tests.unit.helpers import u_test_post_response

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
                    "message": "contract succesfully created",
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
        u_test_post_response(client, TEST_ENDPOINT, data, expected, headers=headers)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {
                "parameters": [
                    {"name": "contract_duration", "value": 12},
                    {"name": "contract_value", "value": 12_000_000},
                    {"name": "start_date", "value": "15-05-2023"},
                    {"name": "notice_period", "value": 3},
                ],
            },
            {
                "status_code": 201,
                "body": {
                    "message": "parameters succesfully created",
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
        u_test_post_response(
            client,
            f"{TEST_ENDPOINT}/{FAKE_OID}/parameters",
            data,
            expected,
            headers=headers,
        )
