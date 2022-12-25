import pytest

from database.users import insert_user
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
    db, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    user = insert_user(data)

    assert user["_id"] == FAKE_OID
    assert user["name"] == expected["name"]
    assert user["username"] == expected["username"]
    assert user["email"] == expected["email"]
    assert user["mobile"] == expected["mobile"]
    assert user["created_at"] == FAKE_TIME
    assert user["password"][:14] == "pbkdf2:sha256:"
