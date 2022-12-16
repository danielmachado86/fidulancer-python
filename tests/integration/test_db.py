import pytest
from testcontainers.mongodb import MongoDbContainer

from tests import FAKE_OID, FAKE_TIME  # pylint: disable=unused-import


@pytest.fixture()
def db():
    """_summary_

    Args:
        app_configuration (_type_): _description_

    Yields:
        _type_: _description_
    """

    with MongoDbContainer("mongo:latest") as mongo:
        client = mongo.get_connection_client()
        yield client


def test_database_connection(
    db,
):  # pylint: disable=redefined-outer-name, missing-function-docstring
    info = db.server_info()
    assert info["ok"] == 1.0
