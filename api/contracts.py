"""_summary_

Returns:
    _type_: _description_
"""

from datetime import datetime

from bson import ObjectId
from flask import Blueprint, current_app, g, jsonify, request, url_for

from api.auth import requires_auth
from api.errors import AuthError, ConflictError, InternalError, NotFoundError
from database.config import app_database
from database.contracts import insert_contract
from database.users import add_object_to_user
from utils.initializers import get_new_date, get_new_objectid

contracts = Blueprint("contracts", __name__)


@contracts.route("/contracts", methods=["POST"])
@requires_auth
def new_contract():
    """Creates new contract

    Returns:
        json: response
        int: http status code
    """

    current_app.logger.info("Creating new contract")
    body = request.get_json()

    insert_contract(body)

    response = jsonify({"message": "contract succesfully created"})
    response.status_code = 201

    return response


@contracts.route("/contracts/<contract_id>/parameters", methods=["POST"])
@requires_auth
def add_contract_parameters(contract_id):
    """Creates new contract

    Returns:
        json: response
        int: http status code
    """

    current_app.logger.info("Creating new contract")
    body = request.get_json()

    add_contract_parameters(body)

    response = jsonify({"message": "contract succesfully created"})
    response.status_code = 201

    return response


@contracts.route("/contracts/<contract_id>", methods=["GET"])
@requires_auth
def get_contract(username, contract_id):
    """Get user

    Returns:
        json: response
        int: http status code
    """

    contract, _ = query_contract(username, contract_id)

    if not contract:
        raise AuthError(
            {
                "code": "unauthorized",
                "description": "authenticated user doesn't owns this resource",
            }
        )

    response = jsonify(contract)
    response.status_code = 200
    return response


@contracts.route("/contracts/<contract_id>/invitations", methods=["POST"])
@requires_auth
def send_invitation(username, contract_id):
    """Get user

    Returns:
        json: response
        int: http status code
    """

    body = request.get_json()
    new_member_username = body["username"]

    _, users = query_contract(username, contract_id)

    not_owner = True
    is_member = False
    for user in users:
        if username == user["username"]:
            not_owner = False
        if new_member_username == user["username"]:
            is_member = True

    if not_owner:
        raise AuthError(
            {
                "code": "unauthorized",
                "description": "authenticated user doesn't owns this resource",
            }
        )

    if is_member:
        raise ConflictError(
            {
                "code": "conflict",
                "description": "This contract is already registered to user",
            }
        )

    invitation = query_user_invitations(new_member_username, contract_id)

    if invitation:
        raise ConflictError(
            {
                "code": "conflict",
                "description": "The user was already invited to this contract. Waiting for acceptance.",
            }
        )

    contract_data = {
        "invitations": {
            "contract": {"_id": ObjectId(contract_id)},
            "created_at": datetime.now(),
            "invited_by": username,
        }
    }
    add_object_to_user(new_member_username, contract_data)

    response = jsonify({"message": "new member invitation sent"})
    response.status_code = 200
    return response


def find_contract(user, contract_id):
    """_summary_

    Args:
        user (_type_): _description_
        contract_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    for contract in user["contracts"]["active"]:
        if ObjectId(contract_id) == contract["_id"]:
            return contract
    return None


def query_contract(username, contract_id):
    """Query contract

    Returns:
        json: response
        int: http status code
    """
    aggregate = [
        {
            "$facet": {
                "contract": [
                    {"$unwind": "$contracts.active"},
                    {"$match": {"contracts._id": ObjectId(contract_id)}},
                    {
                        "$addFields": {
                            "user": {
                                "_id": "$_id",
                                "name": "$name",
                                "username": "$username",
                            },
                        }
                    },
                    {
                        "$group": {
                            "_id": "$contracts.active._id",
                            "users": {"$push": "$user"},
                            "contract": {"$first": "$contracts.active"},
                        }
                    },
                    {
                        "$replaceRoot": {
                            "newRoot": {"$mergeObjects": ["$contract", "$$ROOT"]}
                        }
                    },
                    {"$unset": "contract"},
                    {
                        "$match": {
                            "$and": [
                                {
                                    "users": {
                                        "$elemMatch": {"username": {"$eq": username}}
                                    }
                                },
                                {"_id": ObjectId(contract_id)},
                            ]
                        }
                    },
                    {"$limit": 1},
                ],
                "users": [
                    {"$match": {"contracts.active._id": ObjectId(contract_id)}},
                ],
            }
        }
    ]

    db = app_database.db
    aggregate_response = db.get_collection("user").aggregate(aggregate)

    aggregate_response = aggregate_response.next()

    users = aggregate_response["users"]
    if not users:
        raise NotFoundError(
            {"code": "contract_not_found", "description": "the resource was not found"}
        )

    contract = aggregate_response["contract"]
    return contract, users


def query_user_invitations(username, contract_id):
    """Query contract

    Returns:
        json: response
        int: http status code
    """
    aggregate = [
        {
            "$match": {
                "$and": [
                    {
                        "invitations": {
                            "$elemMatch": {
                                "contract._id": {"$eq": ObjectId(contract_id)}
                            }
                        }
                    },
                    {"username": username},
                ]
            }
        },
        # {"$limit": 1},
    ]

    db = app_database.db
    invitations = []
    for invitation in db.get_collection("user").aggregate(aggregate):
        invitations.append(invitation)

    return invitations
