
from flask import Flask, request
from flask_pymongo import PyMongo
from pydantic import BaseModel

from config import Config


db = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from api import models
    db.init_app(app)

    from api.errors import errors
    app.register_blueprint(errors)
    from api.users import users
    app.register_blueprint(users, url_prefix='/v1')

    # define the shell context
    @app.shell_context_processor
    def shell_context():  # pragma: no cover
        ctx = {'db': db.cx.fidulancer}
        for attr in dir(models):
            model = getattr(models, attr)
            if hasattr(model, '__bases__') and \
                    BaseModel in getattr(model, '__bases__'):
                ctx[attr] = model
        app.logger.info(ctx)
        return ctx

    @app.after_request
    def after_request(response):
        # Werkzeug sometimes does not flush the request body so we do it here
        request.get_data()
        return response
    return app
