"""_summary_

Yields:
    _type_: _description_
"""

import pytest
from flask_pymongo import PyMongo

from api import create_app


@pytest.fixture()
def empty_db():
    """_summary_

    Args:
        app_configuration (_type_): _description_

    Yields:
        _type_: _description_
    """
    app = create_app()

    store = PyMongo()
    store.init_app(app)

    yield store

    store.cx.drop_database(app.config.get("MONGO_DATABASE"))
    store.cx.close()
