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
def db_client():
    """_summary_

    Args:
        app_configuration (_type_): _description_

    Yields:
        _type_: _description_
    """

    with MongoDbContainer("mongo:latest") as mongo:
        client = mongo.get_connection_client()
        yield client


@pytest.fixture()
def db(db_client):

    """_summary_

    Args:
        app_configuration (_type_): _description_

    Yields:
        _type_: _description_
    """

    set_new_objectid(FAKE_OID)
    set_new_date(FAKE_TIME)
    database = db_client.fidulancer
    set_app_database(database)
    yield database
