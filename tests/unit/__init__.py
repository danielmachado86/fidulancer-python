import datetime
from unittest.mock import patch

import mongomock
import pytest

from api.app import create_app
from database.config import app_database
from database.models import CreateUserValidator
from tests import FAKE_OID, FAKE_TIME
from utils.initializers import set_new_date, set_new_objectid

pytest.register_assert_rewrite("tests.unit.helpers")


class PyMongoMock(mongomock.MongoClient):  # pylint: disable=abstract-method
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
    app = create_app()  # pylint: disable=redefined-outer-name
    app.config.update({"TESTING": True})

    db_client = PyMongoMock()
    db_client.init_app(app)
    dbase = db_client.get_database("fidulancer")

    set_new_date(FAKE_TIME)
    set_new_objectid(FAKE_OID)
    app_database.set_database(database=dbase)

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


@pytest.fixture(autouse=True)
def add_users(app):  # pylint: disable=redefined-outer-name
    """_summary_

    Args:
        app (_type_): _description_
    """
    user_data = {
        "name": "Jimena Lopez",
        "username": "jimenalogo",
        "email": "jimenalogo@gmail.com",
        "mobile": "+573046628057",
        "password": "secret",
    }
    with app.test_request_context():
        user = CreateUserValidator(**user_data).get_data()
    db = app_database.db
    db.get_collection("user").insert_one(user)
