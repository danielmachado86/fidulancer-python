"""_summary_

Returns:
    _type_: _description_
"""
from http import HTTPStatus
from typing import Dict

from flask import Blueprint, Response, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from pymongo.errors import DuplicateKeyError

errors = Blueprint("errors", __name__)


# Format error response and append status code.
class NotFoundError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """
    def __init__(self, error: Dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 404

# Format error response and append status code.
class AuthError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """
    def __init__(self, error: Dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 401

# Format error response and append status code.
class PaymentGatewayError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """
    def __init__(self, error: Dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 503

@errors.app_errorhandler(NotFoundError)
def handle_not_found_error(ex: NotFoundError) -> Response:
    """
    serializes the given AuthError as json and sets the response status code accordingly.
    :param ex: an auth error
    :return: json serialized ex response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@errors.app_errorhandler(AuthError)
def handle_auth_error(ex: AuthError) -> Response:
    """
    serializes the given AuthError as json and sets the response status code accordingly.
    :param ex: an auth error
    :return: json serialized ex response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@errors.app_errorhandler(PaymentGatewayError)
def handle_payment_error(ex: PaymentGatewayError) -> Response:
    """
    serializes the given AuthError as json and sets the response status code accordingly.
    :param ex: an auth error
    :return: json serialized ex response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@errors.app_errorhandler(HTTPException)
def http_error(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {
        "code": error.code,
        "message": error.name,
        "description": error.description,
    }, error.code


@errors.app_errorhandler(ValidationError)
def validation_error(result: ValidationError) -> list[Dict]:
    """_summary_

    Args:
        result (ValidationError): _description_

    Returns:
        list[Dict]: _description_
    """
    return [
        extract_error_data(error) for error in result.errors()
    ], HTTPStatus.BAD_REQUEST


@errors.app_errorhandler(DuplicateKeyError)
def unique_violation(error: DuplicateKeyError) -> Dict:
    """_summary_

    Args:
        error (DuplicateKeyError): _description_

    Returns:
        Dict: _description_
    """
    return {"message": error.details["errmsg"]}, HTTPStatus.BAD_REQUEST


def extract_error_data(error: Dict) -> Dict:
    """select dict keys to be included in response

    Args:
        error (Dict): data about validation error found

    Returns:
        Dict: selected keys
    """
    return {"field": error["loc"][0], "message": error["msg"]}
