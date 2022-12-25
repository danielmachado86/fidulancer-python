import pytest

from tests import FAKE_OID, FAKE_TIME  # pylint: disable=unused-import
from tests.integration import db_client


def test_database_connection(
    db_client,
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    info = db_client.server_info()
    assert info["ok"] == 1.0
