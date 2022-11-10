"""_summary_

Returns:
    _type_: _description_
"""
import json
import uuid

import requests
from flask import Blueprint, current_app, jsonify, request

from api.auth import requires_auth
from api.errors import PaymentGatewayError
from api.users import add_payment_method, add_transaction, get_user

funds = Blueprint("funds", __name__)


@funds.route("/payment_methods", methods=["POST"])
@requires_auth
def new_payment_method(username):  # username taken fron requires_auth decorator
    """_summary_

    Returns:
        _type_: _description_
    """
    new_card_body = request.get_json()
    new_card_response = payment_api_post(
        new_card_body, current_app.config.get("PAYMENT_API_PUBLIC_KEY"), "/tokens/cards"
    )
    card_data = new_card_response["data"]
    card_token_id = card_data["id"]

    acceptance_token = get_acceptance_token()

    payment_method_body = {
        "type": "CARD",
        "token": card_token_id,
        "acceptance_token": acceptance_token,
        "customer_email": get_user_email(username),
    }
    payment_method_response = payment_api_post(
        payment_method_body,
        current_app.config.get("PAYMENT_API_PRIVATE_KEY"),
        "/payment_sources",
    )
    payment_method_data = payment_method_response["data"]
    del payment_method_data["token"]
    del payment_method_data["customer_email"]
    del payment_method_data["status"]

    add_payment_method(username, payment_method_data)

    response = jsonify(payment_method_data)
    response.status = 201
    return response


def get_user_email(username):
    """_summary_

    Returns:
        _type_: _description_
    """
    user = get_user(username)
    return user["email"]


@funds.route("/payments", methods=["POST"])
@requires_auth
def new_payment(username):  # username taken fron requires_auth decorator
    """_summary_

    Returns:
        _type_: _description_
    """
    request_body = request.get_json()
    acceptance_token = get_acceptance_token()
    user = get_user(username)

    payment_body = {
        "acceptance_token": acceptance_token,
        "amount_in_cents": int(request_body["amount_in_cents"]),
        "currency": request_body["currency"],
        "customer_email": user["email"],
        "payment_source_id": int(request_body["payment_source_id"]),
        "payment_method": {"installments": int(request_body["installments"])},
        "reference": str(uuid.uuid1()),
    }
    payment_response = payment_api_post(
        payment_body,
        api_key=current_app.config.get("PAYMENT_API_PRIVATE_KEY"),
        endpoint="/transactions",
    )
    payment_data = payment_response["data"]

    add_transaction(username, payment_data)

    response = jsonify(payment_data)
    response.status = 201
    return response


def get_acceptance_token():
    """_summary_

    Returns:
        _type_: _description_
    """
    acceptance_token_url = (
        f'{current_app.config.get("PAYMENT_API_URL")}'
        "/merchants"
        f'/{current_app.config.get("PAYMENT_API_PUBLIC_KEY")}'
    )

    acceptance_token_response = requests.get(acceptance_token_url, timeout=15)
    acceptance_token_json = json.loads(acceptance_token_response.text)
    acceptance_token_data = acceptance_token_json["data"]
    presigned_acceptance = acceptance_token_data["presigned_acceptance"]
    acceptance_token = presigned_acceptance["acceptance_token"]
    return acceptance_token


def payment_api_post(body, api_key, endpoint):
    """_summary_

    Args:
        body (_type_): _description_
        api_key (_type_): _description_
        endpoint (_type_): _description_

    Returns:
        _type_: _description_
    """
    url_source = f'{current_app.config.get("PAYMENT_API_URL")}{endpoint}'
    headers = {"authorization": f"Bearer {api_key}"}
    response = requests.post(
        url_source, data=json.dumps(body), timeout=15, headers=headers
    )
    if response.status_code != 201:
        raise PaymentGatewayError(
            {"code": "internal error", "description": response.reason}
        )
    data = json.loads(response.text)
    return data
