"""_summary_
"""

import pytest

from tests.unit import FAKE_TIME, app, client  # pylint: disable=unused-import


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
                    "name": "Jimena Lopez",
                    "username": "jimenalogo",
                    "email": "jimenalogo@gmail.com",
                    "mobile": "+573046628057",
                    "created_at": FAKE_TIME.isoformat(),
                },
            },
        ),
        (
            {},
            400,
        ),
        (
            {
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
                "password": "secret",
            },
            400,
        ),
        (
            {
                "name": "Jimena Lopez",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
                "password": "secret",
            },
            400,
        ),
        (
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "mobile": "+573046628057",
                "password": "secret",
            },
            400,
        ),
        (
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "password": "secret",
            },
            400,
        ),
        (
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
            },
            400,
        ),
    ],
    ids=[
        "ok",
        "empty_body",
        "missing_name",
        "missing_username",
        "missing_email",
        "missing_mobile",
        "missing_password",
    ],
)
def test_user_registration(
    client, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    response = client.post("/v1/users", json=data)
    # assert response.status_code == expected["status_code"]
    assert response.get_json() == expected["body"]
    # assert isinstance(api.db.datetime.datetime, datetime.datetime) is True
