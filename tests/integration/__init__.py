"""_summary_

Yields:
    _type_: _description_
"""

import pytest
from testcontainers.mongodb import MongoDbContainer

from database.config import set_app_database
from tests import FAKE_OID, FAKE_TIME
from utils.initializers import set_new_date, set_new_objectid


@pytest.fixture()
def db():
    """_summary_

    Args:
        app_configuration (_type_): _description_

    Yields:
        _type_: _description_
    """

    with MongoDbContainer("mongo:latest") as mongo:
        set_new_objectid(FAKE_OID)
        set_new_date(FAKE_TIME)
        client = mongo.get_connection_client()
        database = client.fidulancer
        set_app_database(database)
