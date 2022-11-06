"""_summary_

Returns:
    _type_: _description_
"""
import json

import requests
from flask import Blueprint, current_app, jsonify, request
from api.auth import authenticated_user, requires_auth
from api.errors import PaymentGatewayError

from api.users import get_user, add_payment_method


funds = Blueprint("funds", __name__)

@funds.route("/payment_methods", methods=['POST'])
@requires_auth
def new_payment_method():
    """_summary_

    Returns:
        _type_: _description_
    """
    new_card_body = request.get_json()
    new_card_response = api_post(
        new_card_body,
        current_app.config.get("PAYMENT_API_PUBLIC_KEY"),
        '/tokens/cards'
    )
    card_data = new_card_response['data']
    card_token_id = card_data['id']
    
    acceptance_token_url = (
        f'{current_app.config.get("PAYMENT_API_URL")}'
            '/merchants/'
            f'{current_app.config.get("PAYMENT_API_PUBLIC_KEY")}'
    )

    acceptance_token_response = requests.get(acceptance_token_url, timeout=15)
    acceptance_token_json = json.loads(acceptance_token_response.text)
    acceptance_token_data = acceptance_token_json['data']
    presigned_acceptance = acceptance_token_data['presigned_acceptance']
    acceptance_token = presigned_acceptance['acceptance_token']

    username = authenticated_user['username']
    
    user = get_user(username)

    payment_method_body = {'type': 'CARD',
              'token': card_token_id,
              'acceptance_token': acceptance_token,
              'customer_email': user['email']}
    payment_method_response = api_post(
        payment_method_body,
        current_app.config.get("PAYMENT_API_PRIVATE_KEY"),
        '/payment_sources'
    )
    payment_method_data = payment_method_response['data']
    del payment_method_data['token']
    del payment_method_data['customer_email']
    del payment_method_data['status']

    add_payment_method(username, payment_method_data)

    response = jsonify(payment_method_data)
    response.status = 201
    return response

@funds.route("/payments", methods=['POST'])
@requires_auth
def new_payment():
    """_summary_

    Returns:
        _type_: _description_
    """
    new_card_body = request.get_json()
    new_card_response = api_post(
        new_card_body,
        current_app.config.get("PAYMENT_API_PUBLIC_KEY"),
        '/tokens/cards'
    )
    card_data = new_card_response['data']
    card_token_id = card_data['id']
    
    acceptance_token_url = (
        f'{current_app.config.get("PAYMENT_API_URL")}'
            '/merchants/'
            f'{current_app.config.get("PAYMENT_API_PUBLIC_KEY")}'
    )

    acceptance_token_response = requests.get(acceptance_token_url, timeout=15)
    acceptance_token_json = json.loads(acceptance_token_response.text)
    acceptance_token_data = acceptance_token_json['data']
    presigned_acceptance = acceptance_token_data['presigned_acceptance']
    acceptance_token = presigned_acceptance['acceptance_token']

    username = authenticated_user['username']
    
    user = get_user(username)

    payment_method_body = {'type': 'CARD',
              'token': card_token_id,
              'acceptance_token': acceptance_token,
              'customer_email': user['email']}
    payment_method_response = api_post(
        payment_method_body,
        current_app.config.get("PAYMENT_API_PRIVATE_KEY"),
        '/payment_sources'
    )
    payment_method_data = payment_method_response['data']
    del payment_method_data['token']
    del payment_method_data['customer_email']
    del payment_method_data['status']

    add_payment_method(username, payment_method_data)

    response = jsonify(payment_method_data)
    response.status = 201
    return response

def api_post(body, api_key, endpoint):
    """_summary_

    Args:
        body (_type_): _description_
        api_key (_type_): _description_
        endpoint (_type_): _description_

    Returns:
        _type_: _description_
    """
    url_source = f'{current_app.config.get("PAYMENT_API_URL")}{endpoint}'
    headers = {'authorization': f'Bearer {api_key}'}
    response = requests.post(
        url_source,
        json.dumps(body),
        timeout=15,
        headers=headers
    )
    if response.status_code != 201:
        raise PaymentGatewayError(
            {
                "code": "internal error",
                "description":"Call to payment gateway service failed"
            }
        )
    data = json.loads(response.text)
    return data


