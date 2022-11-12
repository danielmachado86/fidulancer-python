"""_summary_

Returns:
    _type_: _description_
"""


from flask import Flask

from api.db import Store
from config import Config

users_store = Store("mongodb", "user")


def create_app(config_class=Config):
    """_summary_

    Args:
        config_class (_type_, optional): _description_. Defaults to Config.

    Returns:
        _type_: _description_
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    users_store.init_app(app)

    users_store.create_index("username")
    users_store.create_index("email")
    users_store.create_index("mobile")

    from api.errors import errors  # pylint: disable=import-outside-toplevel

    app.register_blueprint(errors)

    from api.users import users  # pylint: disable=import-outside-toplevel

    app.register_blueprint(users, url_prefix="/v1")

    from api.contracts import contracts

    app.register_blueprint(contracts, url_prefix="/v1")

    from api.sessions import sessions  # pylint: disable=import-outside-toplevel

    app.register_blueprint(sessions, url_prefix="/v1")

    from api.payments import funds  # pylint: disable=import-outside-toplevel

    app.register_blueprint(funds, url_prefix="/v1")

    return app
