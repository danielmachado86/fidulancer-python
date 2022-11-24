from tests.integration import empty_db  # pylint: disable=unused-import


def test_database_connection(
    empty_db,
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    info = empty_db.cx.server_info()
    assert info["ok"] == 1.0
