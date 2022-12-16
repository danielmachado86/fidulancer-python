"""_summary_

Yields:
    _type_: _description_
"""

import pytest
from testcontainers.mongodb import MongoDbContainer

from database.config import Database
from tests import FAKE_OID, FAKE_TIME
from utils.initializers import app_date, app_objectid


@pytest.fixture()
def db():
    """_summary_

    Args:
        app_configuration (_type_): _description_

    Yields:
        _type_: _description_
    """

    with MongoDbContainer("mongo:latest") as mongo:
        app_objectid.set_test_value(FAKE_OID)
        app_date.set_test_value(FAKE_TIME)
        client = mongo.get_connection_client()
        database = client.fidulancer
        yield Database(database=database)
