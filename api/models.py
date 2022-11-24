"""models for user api

"""

import datetime

from bson.objectid import ObjectId as bson_ObjectId
from pydantic import BaseModel, EmailStr, validator
from pydantic.dataclasses import dataclass
from werkzeug.security import check_password_hash, generate_password_hash


class ObjectId(bson_ObjectId):  # pylint: disable=missing-class-docstring
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, obj):  # pylint: disable=missing-function-docstring
        if not isinstance(obj, bson_ObjectId):
            raise TypeError("ObjectId required")
        return str(obj)


class PaswordValidator(BaseModel):
    """Model definition used in the request for user creation

    Args:
        BaseModel: Pydantic parent class
    """

    password: str

    @validator("password")
    def hash_password(cls, password: str) -> str:
        return generate_password_hash(password)

    def get_data(self):
        return self.dict()


class UserModelValidator(BaseModel):
    """Model definition used in the request for user creation

    Args:
        BaseModel: Pydantic parent class
    """

    name: str
    username: str
    email: EmailStr
    mobile: str
    created_at: datetime.datetime = None

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    @validator("name")
    def name_must_contain_space(cls, v):
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    @validator("created_at", pre=True, always=True)
    def set_created_at_now(cls, v):
        return v or datetime.datetime.now()

    def get_data(self):
        return self.dict()


@dataclass
class UpdateUserModel(BaseModel):
    """Model definition used in the request for user creation

    Args:
        BaseModel: Pydantic parent class
    """

    name: str
    email: EmailStr
    mobile: str


@dataclass
class ChangeUserPasswordModel(BaseModel):
    """Model definition used in the request for user creation

    Args:
        BaseModel: Pydantic parent class
    """

    old: str
    new: str


@dataclass
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
    created_at: datetime.datetime
    updated_at: datetime.datetime
