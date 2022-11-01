from datetime import datetime, timedelta

import jwt
from bson import ObjectId
from flask import Blueprint, abort, current_app, jsonify, request
from werkzeug.security import check_password_hash

from api import user_store
from api.db import JSONEncoder
from api.users import user_response

sessions = Blueprint("sessions", __name__)

session_coll = user_store.database.get_collection("session")



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
        
    payload = payload = jwt.decode(
        jwt=refresh_token,
        key=current_app.config["SECRET_KEY"],
        algorithms=["HS256", "HS512"],
    )
    current_app.logger.info(payload)
    session = session_coll.find_one({"_id": ObjectId(payload['id'])})
    if session is None:
        return abort(404, "session not found")
    access_token_expires_at = datetime.utcnow() \
        + timedelta(
            minutes=current_app.config["ACCESS_TOKEN_MINUTES"]
        )
    access_token = jwt.encode(
        payload={
            "username": payload['username'],
            "exp": access_token_expires_at,
        },
        key=current_app.config["SECRET_KEY"],
        algorithm="HS512",
        json_encoder=JSONEncoder,
    )

    response = jsonify({
        "access_token": access_token,
        "access_token_expires_ at": access_token_expires_at,
    })
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
    username = data.get("username")
    password = data.get("password")
    if username is None or password is None:
        abort(400, "username and password are required")
    user = user_store.get_user(username)
    current_app.logger.info(user)
    if user is None or not check_password_hash(user.get("hashed_password"), password):
        return abort(401, "username and password incorrect")
    access_token_expires_at = datetime.utcnow() \
        + timedelta(
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
    
    session_id = ObjectId()

    refresh_token_expires_at = datetime.utcnow() \
        + timedelta(
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

    result = session_coll.insert_one({
        "_id": session_id,
        "username": username,
        "refresh_token": refresh_token,
        "user_agent": request.user_agent.string,
        "client_ip": request.remote_addr,
        "is_active": True,
        "expires_ at": refresh_token_expires_at,
    })

    response = jsonify({
        "id": result.inserted_id,
        "access_token": access_token,
        "access_token_expires_ at": access_token_expires_at,
        "refresh_token": refresh_token,
        "refresh_token_expires_ at": refresh_token_expires_at,
        "user": user_response(user),
        "is_active": True,
    })
    response.status_code = 201
    return response
