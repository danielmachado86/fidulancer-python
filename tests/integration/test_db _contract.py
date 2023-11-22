import pytest
from pymongo.database import Database

from database.users import insert_user, update_user
from tests import FAKE_OID, FAKE_TIME
from tests.integration import db, db_client  # pylint: disable=unused-import


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
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
            },
        ),
    ],
    ids=[
        "ok",
    ],
)
def test_insert_user_ok(
    db: Database,  # pylint: disable=invalid-name,unused-argument
    data: dict[str, str],
    expected: dict[str, str],
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    user = insert_user(data)

    assert user["_id"] == FAKE_OID
    assert user["name"] == expected["name"]
    assert user["username"] == expected["username"]
    assert user["email"] == expected["email"]
    assert user["mobile"] == expected["mobile"]
    assert user["created_at"] == FAKE_TIME
    assert user["password"][:14] == "pbkdf2:sha256:"


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
            },
            {
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
            },
        ),
    ],
    ids=[
        "ok",
    ],
)
def test_update_user_ok(
    db: Database,  # pylint: disable=invalid-name,unused-argument
    data: dict[str, str],
    expected: dict[str, str],
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    user = update_user(username, data)

    assert user["_id"] == FAKE_OID
    assert user["name"] == expected["name"]
    assert user["username"] == expected["username"]
    assert user["email"] == expected["email"]
    assert user["mobile"] == expected["mobile"]
    assert user["created_at"] == FAKE_TIME
    assert user["password"][:14] == "pbkdf2:sha256:"
