"""_summary_
"""

from werkzeug.routing import BaseConverter
from bson import ObjectId
from bson.errors import InvalidId
from flask import abort


class MongoObjectId(BaseConverter):
    """_summary_

    Args:
        BaseConverter (_type_): _description_
    """

    def to_python(self, value: str) -> ObjectId:
        try:
            return ObjectId(value)
        except InvalidId as exc:
            raise abort(404) from exc  # pylint: disable=raising-bad-type

    def to_url(self, value: ObjectId) -> str:
        return str(value)
