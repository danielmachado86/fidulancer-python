import datetime
from unittest.mock import patch

import pytest
from mongomock import MongoClient

import api
from api.app import app_date, app_objectid, create_app
from api.db import CustomJSONProvider

pytest.register_assert_rewrite("tests.unit.helpers")

FAKE_TIME = datetime.datetime(2022, 12, 25, 17, 5, 55)
FAKE_OID = "6385248afe09c73d411fda0a"


class PyMongoMock(MongoClient):  # pylint: disable=abstract-method
    """_summary_

    Args:
        MongoClient (_type_): _description_
    """

    def init_app(
        self, app
    ):  # pylint: disable=missing-function-docstring,redefined-outer-name,unused-argument
        return super().__init__()


@pytest.fixture()
def app():
    """_summary_

    Yields:
        _type_: _description_
    """
    with patch.object(
        api.db,
        "store",
        PyMongoMock(),
    ):
        app = create_app()  # pylint: disable=redefined-outer-name
        app_date.new_date(FAKE_TIME)
        app_objectid.new_value(FAKE_OID)
        app.config.update({"TESTING": True})
        yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):  # pylint: disable=redefined-outer-name
    """_summary_

    Args:
        app (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!
