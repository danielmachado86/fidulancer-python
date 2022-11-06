# pylint: disable=no-member

"""User endpoints definition

"""

from datetime import datetime
from typing import Dict

from flask import Blueprint, current_app, jsonify, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from api import user_store
from api.auth import authenticated_user, requires_auth
from api.errors import AuthError, NotFoundError
from api.models import (ChangeUserPasswordRequest, CreateUserRequest,
                        UpdateUserRequest, validate_model)

users = Blueprint("users", __name__)


def user_response(user: Dict):
    """_summary_

    Args:
        user (Dict): _description_

    Returns:
        _type_: _description_
    """
    if 'password' in user:
        del user['password']
    if 'hashed_password' in user:
        del user['hashed_password']
    return user


@users.route("/users/<username>", methods=["GET"])
@requires_auth
def get_user_response(username):
    """Get user

    Returns:
        json: response
        int: http status code
    """

    if authenticated_user['username'] != username:
        raise AuthError({"code": "unauthorized",
                        "description":
                            "the authenticated user is not authorized"
                            " to view this resource"})

    user = get_user(username)

    response = jsonify(user_response(user))
    response.status_code = 200
    return response


@users.route("/users/<username>", methods=["PUT"])
@requires_auth
def update_user_info(username):
    """Get user

    Returns:
        json: response
        int: http status code
    """

    if authenticated_user['username'] != username:
        raise AuthError({"code": "unauthorized",
                        "description":
                            "the authenticated user is not authorized"
                            " to view this resource"})

    _ = get_user(username)

    body = request.get_json()

    # If not valid pydantic.ValidationError is raised
    validate_model(UpdateUserRequest, body)

    rsp = user_store.update_user(username, body)

    response = jsonify(rsp.upserted_id)
    response.headers["Location"] = url_for(
        "users.update_user_response", username=body["username"])
    response.status_code = 200
    return response


@users.route("/users/<username>/password", methods=["POST"])
@requires_auth
def update_user_password(username):
    """Update user password

    Returns:
        json: response
        int: http status code
    """

    if authenticated_user['username'] != username:
        raise AuthError({"code": "unauthorized",
                        "description":
                            "the authenticated user is not authorized"
                            " to view this resource"})

    user = get_user(username)

    body = request.get_json()

    # If not valid pydantic.ValidationError is raised
    validate_model(ChangeUserPasswordRequest, body)

    match = check_password_hash(user.get("hashed_password"), body["old"])
    if not match:
        raise AuthError({"code": "unauthorized",
                        "description":
                            "old password doesn't match"})

    password = {"hashed_password": generate_password_hash(body["new"])}

    rsp = user_store.update_user(username, password)

    response = jsonify(rsp.upserted_id)
    response.status_code = 200
    return response


def get_user(username):
    """Get user

    Returns:
        json: response
        int: http status code
    """
    user = user_store.get_user(username)
    if user is None:
        raise NotFoundError({"code": "user_not_found",
                            "description":
                                "the resource was not found"})
    return user


@users.route("/users", methods=["POST"])
def new_user():
    """Creates new user

    Returns:
        json: response
        int: http status code
    """

    current_app.logger.info("Creating new item")
    body = request.get_json()

    # If not valid pydantic.ValidationError is raised
    validate_model(CreateUserRequest, body)

    body["hashed_password"] = generate_password_hash(body["password"])

    body["created_at"] = datetime.now()
    body["updated_at"] = datetime.min

    # Unique constraint checked using pymongo.errors.DuplicateKeyError
    user_store.insert_user(body)

    # Remove password and hashed_paswords from user object
    response = user_response(body)

    response = jsonify(response)
    response.status_code = 201
    response.headers["Location"] = url_for(
        "users.get_user_response", username=body["username"])
    return response


def add_payment_method(username, payment_method_data):
    """_summary_

    Args:
        username (_type_): _description_
        card_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    rsp = user_store.add_to_list(
        username=username,
        data={
            'payment_method': payment_method_data
        }
    )

    return rsp
