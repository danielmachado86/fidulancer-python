from http import HTTPStatus
from typing import Dict
from flask import Blueprint, current_app
from werkzeug.exceptions import HTTPException, InternalServerError
from pydantic import ValidationError

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(HTTPException)
def http_error(error):
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code


@errors.app_errorhandler(ValidationError)
def validation_error(result):
    return [extract_error_data(error) for error in result.errors()] , HTTPStatus.BAD_REQUEST



def extract_error_data(error: Dict) -> Dict:
    """select dict keys to be included in response

    Args:
        error (Dict): data about validation error found

    Returns:
        Dict: selected keys
    """
    return {
        "field": error["loc"][0],
        "message": error["msg"]
    }
