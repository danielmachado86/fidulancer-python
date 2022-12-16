"""_summary_

Returns:
    _type_: _description_
"""
from api.errors import InternalError, NotFoundError
from database.config import app_database
from database.models import CreateUserValidator


def insert_user(data):
    """_summary_

    Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """

    # If not valid pydantic.ValidationError is raised
    model_validation = CreateUserValidator(**data)
    user = model_validation.get_data()

    # Unique constraint checked using mongodb indexes
    db = app_database.db
    result = db.get_collection("user").insert_one(user)
    oid = result.inserted_id
    if not oid:
        raise InternalError(
            {"code": "internal-error", "message": "database insertion error"}
        )
    user["_id"] = oid
    return user


def update_user(username, data):
    """Update user

    Returns:
        json: response
        int: http status code
    """
    newvalues = {"$set": data}
    user_filter = {"username": username}

    db = app_database.db
    result = db.get_collection("user").update_one(user_filter, newvalues)
    return result


def get_user(username):
    """Get user

    Returns:
        json: response
        int: http status code
    """
    db = app_database.db
    user = db.get_collection("user").find_one({"username": username})
    if user is None:
        raise NotFoundError(
            {"code": "user_not_found", "description": "the resource was not found"}
        )
    return user


def add_object_to_user(username, data):
    """Update user

    Returns:
        json: response
        int: http status code
    """
    newvalues = {"$push": data}
    user_filter = {"username": username}

    db = app_database.db
    result = db.get_collection("user").update_one(user_filter, newvalues)
    return result
