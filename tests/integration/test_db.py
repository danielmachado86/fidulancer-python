import pytest

from database.users import insert_user
from tests import FAKE_OID, FAKE_TIME  # pylint: disable=unused-import
from tests.integration import empty_db


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
                "status_code": 201,
                "body": {
                    "_id": FAKE_OID,
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
def test_inser_user_ok(
    empty_db, data, expected
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    user = insert_user(data)
    assert user == expected
