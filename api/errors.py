"""_summary_

Returns:
    _type_: _description_
"""
from http import HTTPStatus

from flask import Blueprint, Response, current_app, jsonify
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError

errors = Blueprint("errors", __name__)


# Format error response and append status code.
class NotFoundError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """

    def __init__(self, error: dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 404


# Format error response and append status code.
class BadRequestError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """

    def __init__(self, error: dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 400


# Format error response and append status code.
class InternalError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """

    def __init__(self, error: dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 500


# Format error response and append status code.
class ConflictError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """

    def __init__(self, error: dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 409


# Format error response and append status code.
class AuthError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """

    def __init__(self, error: dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 401


# Format error response and append status code.
class PaymentGatewayError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """

    def __init__(self, error: dict[str, str]):
        super().__init__()
        self.error = error
        self.status_code = 503


@errors.app_errorhandler(ConflictError)
def handle_conflict_error(ex: ConflictError) -> Response:
    """
    serializes the given AuthError as json and sets the response status code accordingly.
    :param ex: an auth error
    :return: json serialized ex response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@errors.app_errorhandler(BadRequestError)
def handle_bad_request_error(ex: BadRequestError) -> Response:
    """
    serializes the given AuthError as json and sets the response status code accordingly.
    :param ex: an auth error
    :return: json serialized ex response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


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


@errors.app_errorhandler(ValidationError)
def validation_error(result: ValidationError) -> list[dict]:
    """_summary_

    Args:
        result (ValidationError): _description_

    Returns:
        list[dict]: _description_
    """
    current_app.logger.debug(result.errors())
    return [
        extract_error_data(error) for error in result.errors()
    ], HTTPStatus.BAD_REQUEST


@errors.app_errorhandler(DuplicateKeyError)
def unique_violation(error: DuplicateKeyError) -> dict:
    """_summary_

    Args:
        error (DuplicateKeyError): _description_

    Returns:
        dict: _description_
    """
    return {"message": error.details["errmsg"]}, HTTPStatus.BAD_REQUEST


def extract_error_data(error: dict) -> dict:
    """select dict keys to be included in response

    Args:
        error (dict): data about validation error found

    Returns:
        dict: selected keys
    """
    return {"field": error["loc"][0], "message": error["msg"]}
