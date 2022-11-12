"""_summary_

Returns:
    _type_: _description_
"""

from datetime import datetime

from bson import ObjectId
from flask import Blueprint, current_app, jsonify, request, url_for

from api import users_store
from api.auth import requires_auth
from api.errors import NotFoundError
from api.users import get_user

contracts = Blueprint("contracts", __name__)


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

    contract = {**body}

    contract_id = ObjectId()
    contract.update(_id=contract_id, created_at=datetime.now())

    new_contract_data = {"contracts": contract}
    users_store.add_to_list(username, new_contract_data)

    response = jsonify(contract)
    response.status_code = 201
    response.headers["Location"] = url_for(
        "contracts.get_contract", contract_id=contract_id, username=username
    )
    return response


@contracts.route("/contracts/<contract_id>", methods=["GET"])
@requires_auth
def get_contract(username, contract_id):
    """Get user

    Returns:
        json: response
        int: http status code
    """

    contract = query_contract(username, contract_id).next()

    response = jsonify(contract)
    response.status_code = 200
    return response


def query_contract(username, contract_id):
    """Get user

    Returns:
        json: response
        int: http status code
    """
    user = users_store.collection.aggregate(
        [
            {"$match": {"contracts._id": ObjectId(contract_id)}},
            {"$addFields": {"contracts.users": []}},
            {
                "$replaceRoot": {
                    "newRoot": {
                        "$arrayElemAt": [
                            {
                                "$filter": {
                                    "input": "$contracts",
                                    "cond": {
                                        "$eq": ["$$this._id", ObjectId(contract_id)]
                                    },
                                }
                            },
                            0,
                        ]
                    }
                }
            },
        ]
    )
    if user is None:
        raise NotFoundError(
            {"code": "user_not_found", "description": "the resource was not found"}
        )
    return user
