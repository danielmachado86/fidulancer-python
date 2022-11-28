"""_summary_

Returns:
    _type_: _description_
"""


import datetime

from flask import Flask

from api.db import CustomJSONProvider, store
from config import Config


class Date:
    def __init__(self) -> None:
        self.date = datetime.datetime.now()

    def new_date(self, date):
        self.date = date


app_date = Date()


def get_date():
    return app_date.date


def create_app(config_class=Config) -> Flask:
    """_summary_

    Args:
        config_class (_type_, optional): _description_. Defaults to Config.

    Returns:
        _type_: _description_
    """

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json = CustomJSONProvider(app)

    store.init_app(app)

    from api.errors import errors  # pylint: disable=import-outside-toplevel

    app.register_blueprint(errors)

    from api.users import users  # pylint: disable=import-outside-toplevel

    app.register_blueprint(users, url_prefix="/v1")

    from api.contracts import contracts  # pylint: disable=import-outside-toplevel

    app.register_blueprint(contracts, url_prefix="/v1")

    from api.sessions import sessions  # pylint: disable=import-outside-toplevel

    app.register_blueprint(sessions, url_prefix="/v1")

    from api.payments import funds  # pylint: disable=import-outside-toplevel

    app.register_blueprint(funds, url_prefix="/v1")

    return app
