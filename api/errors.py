from flask import Blueprint, current_app
from werkzeug.exceptions import HTTPException, InternalServerError

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(HTTPException)
def http_error(error):
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code
