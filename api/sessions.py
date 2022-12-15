import json
from datetime import datetime, timedelta

import jwt
from bson import ObjectId
from flask import Blueprint, abort, current_app, jsonify, request
from werkzeug.security import check_password_hash

from api.app import get_app_database, get_new_date, get_new_objectid
from api.errors import BadRequestError, InternalError
from api.models import CredentialsModel, UserResponse

sessions = Blueprint("sessions", __name__)


class JSONEncoder(json.JSONEncoder):
    """_summary_

    Args:
        json (_type_): _description_
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def check_user_password(username, password):
    if username is None or password is None:
        abort(400, "username and password are required")
    db = get_app_database().db
    user_data = db.get_collection("user").find_one({"username": username})
    if user_data is None or not check_password_hash(
        user_data.get("password"), password
    ):
        return abort(401, "username and password incorrect")
    user_response = UserResponse(**user_data)
    return user_response.get_data()


@sessions.route("/sessions/refresher", methods=["POST"])
def refresh_access_token():
    """Creates new user

    Returns:
        json: response
        int: http status code
    """
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    if refresh_token is None:
        abort(400, "refresh_token is required")

    payload = jwt.decode(
        jwt=refresh_token,
        key=current_app.config["SECRET_KEY"],
        algorithms=["HS256", "HS512"],
    )
    db = get_app_database().db
    session = db.get_collection("session").find_one({"_id": ObjectId(payload["id"])})
    if session is None:
        return abort(404, "session not found")
    access_token_expires_at = datetime.utcnow() + timedelta(
        minutes=current_app.config["ACCESS_TOKEN_MINUTES"]
    )
    access_token = jwt.encode(
        payload={
            "username": payload["username"],
            "exp": access_token_expires_at,
        },
        key=current_app.config["SECRET_KEY"],
        algorithm="HS512",
        json_encoder=JSONEncoder,
    )

    response = jsonify(
        {
            "access_token": access_token,
            "access_token_expires_ at": access_token_expires_at,
        }
    )
    response.status_code = 201
    return response


@sessions.route("/sessions", methods=["POST"])
def new_session():
    """Creates new user

    Returns:
        json: response
        int: http status code
    """
    data = request.get_json()

    check_empty_body(data)

    credentials = CredentialsModel(**data).get_data()
    username = credentials["username"]
    password = credentials["password"]

    user = check_user_password(username, password)

    access_token_expires_at = get_new_date() + timedelta(
        minutes=current_app.config["ACCESS_TOKEN_MINUTES"]
    )
    access_token = jwt.encode(
        payload={
            "username": username,
            "exp": access_token_expires_at,
        },
        key=current_app.config["SECRET_KEY"],
        algorithm="HS512",
        json_encoder=JSONEncoder,
    )

    session_id = get_new_objectid()

    refresh_token_expires_at = get_new_date() + timedelta(
        days=current_app.config["REFRESH_TOKEN_DAYS"]
    )
    refresh_token = jwt.encode(
        payload={
            "id": session_id,
            "username": username,
            "exp": refresh_token_expires_at,
        },
        key=current_app.config["SECRET_KEY"],
        algorithm="HS512",
        json_encoder=JSONEncoder,
    )

    db = get_app_database().db
    result = db.get_collection("session").insert_one(
        {
            "_id": session_id,
            "username": username,
            "refresh_token": refresh_token,
            "user_agent": request.user_agent.string,
            "client_ip": request.remote_addr,
            "is_active": True,
            "expires_ at": refresh_token_expires_at,
        }
    )
    oid = result.inserted_id

    if not oid:
        raise InternalError(
            {"code": "internal-error", "message": "database insertion error"}
        )

    response = jsonify(
        {
            "id": oid,
            "access_token": access_token,
            "access_token_expires_ at": access_token_expires_at,
            "refresh_token": refresh_token,
            "refresh_token_expires_ at": refresh_token_expires_at,
            "user": user,
            "is_active": True,
        }
    )
    response.status_code = 201
    return response


def check_empty_body(data):
    if not isinstance(data, dict):
        raise BadRequestError(
            {"code": "empty-request", "message": "request body must be a valid json"}
        )
