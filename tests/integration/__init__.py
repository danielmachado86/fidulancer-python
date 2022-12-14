"""_summary_

Yields:
    _type_: _description_
"""

import pytest
from testcontainers.mongodb import MongoDbContainer


@pytest.fixture()
def empty_db():
    """_summary_

    Args:
        app_configuration (_type_): _description_

    Yields:
        _type_: _description_
    """

    with MongoDbContainer("mongo:latest") as mongo:

        yield mongo.get_connection_client()
