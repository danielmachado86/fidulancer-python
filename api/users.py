# pylint: disable=no-member

from flask import Blueprint, current_app, jsonify, request
from api.models import User

users = Blueprint('users', __name__)


@users.route('/users', methods=['GET'])
def get_user():
    current_app.logger.info("Quering all users")
    page = int(request.args.get('page',3))
    limit = int(request.args.get('limit',2))
    result = User.objects.paginate(page=page, per_page=limit)
    return jsonify(result.items), 200


@users.route('/users', methods=['POST'])
def new_user():
    current_app.logger.info("Creating new item")
    body = request.get_json()
    user = User(**body).save()
    return jsonify(user), 201
