# pylint: disable=no-member

import json
from flask import Blueprint, current_app, request
from bson import json_util
from api import db
from api.models import User

users = Blueprint('users', __name__)

def objectid(item):
    item["id"] = str(item["_id"])

@users.route('/users', methods=['GET'])
def get_user():
    current_app.logger.info("Quering all users")
    result = list(db.cx.fidulancer.user.find({}))
    list(map(objectid, result))
    current_app.logger.info(result)
    return json.loads(json_util.dumps(result)), 200


@users.route('/users', methods=['POST'])
@validate(body=User)
def new_user():
    current_app.logger.info("Creating new item")
    body = request.get_json()
    user =  User(**body)
    current_app.logger.info(user)
    result = db.cx.fidulancer.user.insert_one(user)
    return json.loads(json_util.dumps(result.inserted_id)), 201
