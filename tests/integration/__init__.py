"""_summary_

Yields:
    _type_: _description_
"""

from typing import Generator

import pytest
from pymongo import MongoClient
from pymongo.database import Database
from testcontainers.mongodb import MongoDbContainer

from api.app import app_database
from tests import FAKE_OID, FAKE_TIME
from utils.initializers import set_new_date, set_new_objectid


@pytest.fixture()
def db_client() -> Generator[MongoClient, None, None]:
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
def db(  # pylint: disable=invalid-name
    db_client: MongoClient,  # pylint: disable=redefined-outer-name
) -> Generator[Database, None, None]:

    """_summary_

    Args:
        app_configuration (_type_): _description_

    Yields:
        _type_: _description_
    """

    set_new_objectid(FAKE_OID)
    set_new_date(FAKE_TIME)
    database = db_client.fidulancer
    app_database.set_database(database)
    yield database
