"""_summary_

Returns:
    _type_: _description_
"""

from datetime import datetime

from bson import ObjectId
from flask import Blueprint, current_app, jsonify, request, url_for

from api import users_store
from api.auth import requires_auth

contracts = Blueprint("users", __name__)


@contracts.route("/contracts", methods=["POST"])
@requires_auth
def new_contract(username):
    """Creates new contract

    Returns:
        json: response
        int: http status code
    """

    current_app.logger.info("Creating new contract")
    body = request.get_json()

    body["_id"] = ObjectId()
    body["created_at"] = datetime.now()
    body["updated_at"] = datetime.min

    dic = {"contracts": {"_id": ObjectId()}}
    users_store.add_to_list(username, dic)

    # Remove password and hashed_paswords from user object

    response = jsonify(body)
    response.status_code = 201
    response.headers["Location"] = url_for(
        "users.get_user_response", username=body["username"]
    )
    return response
