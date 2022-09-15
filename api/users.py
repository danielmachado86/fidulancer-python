# pylint: disable=no-member

"""User endpoints definition

"""

from datetime import datetime
import json
from flask import Blueprint, current_app, request
from bson import json_util
from api import db
from api.models import UserRequest, UserResponse, validate_model

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def get_user():
    """Get user list

    Returns:
        json: response
        int: http status code
    """
    current_app.logger.info("Quering all users")

    results = []
    for result in db.cx.fidulancer.user.find({}):
        validate_model(UserResponse, result)
        results.append(result)

    current_app.logger.info(results)
    return json.loads(json_util.dumps(results)), 200


@users.route('/users', methods=['POST'])
def new_user():
    """Creates new user

    Returns:
        json: response
        int: http status code
    """
    current_app.logger.info("Creating new item")
    body = request.get_json()

    validate_model(UserRequest, body)

    body["created_at"] = datetime.now()
    body["updated_at"] = datetime.min

    save_result = db.cx.fidulancer.user.insert_one(body)

    current_app.logger.info(save_result.inserted_id)
    return json.loads(json_util.dumps(save_result.inserted_id)), 201
