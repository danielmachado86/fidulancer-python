import pytest

from database.users import insert_user
from tests import FAKE_OID, FAKE_TIME  # pylint: disable=unused-import
from tests.integration import db


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
                "_id": FAKE_OID,
                "name": "Jimena Lopez",
                "username": "jimenalogo",
                "email": "jimenalogo@gmail.com",
                "mobile": "+573046628057",
                "created_at": FAKE_TIME.isoformat(),
                "password": "secret",
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
    assert user == expected
