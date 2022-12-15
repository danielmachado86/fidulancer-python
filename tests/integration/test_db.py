import pytest

from tests import FAKE_OID, FAKE_TIME  # pylint: disable=unused-import
from tests.integration import db


def test_database_connection(
    empty_db,
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    info = empty_db.server_info()
    assert info["ok"] == 1.0


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
    user = db.insert_user(data)
    assert user == expected
