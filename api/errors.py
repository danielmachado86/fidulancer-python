from http import HTTPStatus
from flask import Blueprint, current_app
from werkzeug.exceptions import HTTPException, InternalServerError
from mongoengine import ValidationError

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(HTTPException)
def http_error(error):
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code

@errors.app_errorhandler(ValidationError)
def validation_error(error):
    fields = [field for field in error.errors]
    return {
        'code': HTTPStatus.BAD_REQUEST,
        'message': error.message,
        'fields': fields,
    }, HTTPStatus.BAD_REQUEST
