import json
from flask import Blueprint, current_app
from bson.json_util import dumps

from api import collection

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def get_user():
    current_app.logger.info("Quering table")
    result = collection.find()
    return json.loads(dumps(result))

@users.route('/users', methods=['POST'])
def new_user():
    current_app.logger.info("Creating new item")
    user = {
        'pk': 'USER#hmachador',
        'sk': 'PROFILE',
        'firstName': "Humberto",
        "lastName": "Machado",
        "username": "hmachador",
        "email": "hmachador@gmail.com",
    }
    result = collection.insert_one(user)
    return json.loads(dumps(result.inserted_id))
