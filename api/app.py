"""_summary_

Returns:
    _type_: _description_
"""


from flask import Flask

from config import Config
from api.db import Store


user_store = Store("mongodb", "user")
contract_store = Store("mongodb", "contract")


def create_app(config_class=Config):
    """_summary_

    Args:
        config_class (_type_, optional): _description_. Defaults to Config.

    Returns:
        _type_: _description_
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    user_store.init_app(app)
    contract_store.init_app(app)
    
    user_store.create_index("username")
    user_store.create_index("email")
    user_store.create_index("mobile")

    from api.errors import errors  # pylint: disable=import-outside-toplevel
    app.register_blueprint(errors)
    
    from api.users import users  # pylint: disable=import-outside-toplevel
    app.register_blueprint(users, url_prefix="/v1")
    
    from api.sessions import sessions  # pylint: disable=import-outside-toplevel
    app.register_blueprint(sessions, url_prefix="/v1")

    return app
