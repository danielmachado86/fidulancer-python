"""_summary_
"""
import datetime

import pytest

import api
from tests.unit import app, client  # pylint: disable=unused-import

FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(api.models.datetime, "datetime", mydatetime)


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
    client, patch_datetime_now, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    response = client.post("/v1/users", json=data)
    # assert response.status_code == expected["status_code"]
    assert response == expected["body"]
    assert api.models.datetime.datetime.now() == FAKE_TIME
