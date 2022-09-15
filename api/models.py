"""models for user api

"""

import datetime
from typing import Dict
from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId as bson_ObjectId


class Config:
    """ Config pydantic
    """
    validate_assignment = True

class ObjectId(bson_ObjectId):
    """_summary_

    Args:
        bson_ObjectId (_type_): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, obj):
        """_summary_

        Args:
            v (_type_): _description_

        Raises:
            TypeError: _description_

        Returns:
            _type_: _description_
        """
        if not isinstance(obj, bson_ObjectId):
            raise TypeError('ObjectId required')
        return str(obj)


class UserRequest(BaseModel):
    """Model definition used in the request for user creation

    Args:
        BaseModel: Pydantic parent class
    """
    name: str
    username: str
    email: EmailStr
    mobile: str
    password: str


class UserResponse(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    _id: ObjectId
    name: str
    username: str
    email: EmailStr
    mobile: str
    password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

def validate_model(model: BaseModel, data: Dict) -> None:
    """_summary_

    Args:
        model (BaseModel): Pydantic model class
        data (Dict): data to be validated

    Returns:
        List[Dict]: errors to be included in response
    """
    model(**data)
