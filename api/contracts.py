"""_summary_

Returns:
    _type_: _description_
"""

from datetime import datetime

from bson import ObjectId
from flask import Blueprint, current_app, jsonify, request, url_for

from api import users_store
from api.auth import requires_auth
from api.errors import AuthError, NotFoundError

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

    contract = query_contract(username, contract_id)

    response = jsonify(contract)
    response.status_code = 200
    return response


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
                    {"$unwind": "$contracts"},
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
                            "_id": "$contracts._id",
                            "users": {"$push": "$user"},
                            "contract": {"$first": "$contracts"},
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
                "found": [
                    {"$match": {"contracts._id": ObjectId(contract_id)}},
                    {"$project": {"contracts": 1}},
                ],
            }
        }
    ]

    aggregate_response = users_store.collection.aggregate(aggregate)

    aggregate_response = aggregate_response.next()

    found = aggregate_response["found"]
    if not found:
        raise NotFoundError(
            {"code": "contract_not_found", "description": "the resource was not found"}
        )

    contract = aggregate_response["contract"]
    if not contract:
        raise AuthError(
            {
                "code": "unauthorized",
                "description": "authenticated doesn't owns this resource",
            }
        )
    return contract
