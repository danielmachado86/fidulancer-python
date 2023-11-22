"""_summary_

Returns:
    _type_: _description_
"""
from bson import ObjectId

from api.errors import InternalError, NotFoundError
from database.config import app_database


def insert_contract(user_id, new_contract):
    """_summary_

    Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Unique constraint checked using mongodb indexes
    db = app_database.get_app_database()
    result = db.get_collection("user").update_one(
        {"_id": ObjectId(user_id)}, {"$push": {"contracts": new_contract}}
    )
    if result.modified_count == 1:
        return True

    return False


def insert_contract_parameters(contract_id, data):
    """_summary_

        Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """

    newvalues = {"$push": data}
    contract_filter = {"contract._id": ObjectId(contract_id)}

    # Unique constraint checked using mongodb indexes
    db = app_database.get_app_database()
    db.get_collection("user").update_one(contract_filter, newvalues)
