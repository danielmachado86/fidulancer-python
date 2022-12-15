from api.errors import InternalError
from api.models import CreateUserValidator


class Database:
    def __init__(self, database=None) -> None:
        self.db = database

    def set_database(self, database):
        self.db = database

    def insert_user(self, data):
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
        result = self.db.get_collection("user").insert_one(user)
        oid = result.inserted_id
        if not oid:
            raise InternalError(
                {"code": "internal-error", "message": "database insertion error"}
            )
        user["_id"] = oid
        return user
