"""models for user api

"""

import datetime
from typing import Dict
from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId as bson_ObjectId


class Config:
    validate_assignment = True

class ObjectId(bson_ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not isinstance(v, bson_ObjectId):
            raise TypeError('ObjectId required')
        return str(v)


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
