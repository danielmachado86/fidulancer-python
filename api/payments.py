"""_summary_

Returns:
    _type_: _description_
"""
import json

import requests
from flask import Blueprint, current_app, jsonify, request

funds = Blueprint("funds", __name__)

@funds.route("/funds", methods=['POST'])
def place_funds():
    """_summary_

    Returns:
        _type_: _description_
    """
    url = f'{current_app.config.get("PAYMENT_API_URL")}/tokens/cards'
    
    data = request.get_json()
    current_app.logger.debug(data)
    payment_auth_header = f'Bearer {current_app.config.get("PAYMENT_API_AUTH_TOKEN")}'
    headers = {'authorization': payment_auth_header}
    response = requests.post(url, json.dumps(data), timeout=15, headers=headers)
    pmnt = json.loads(response.text)
    return jsonify({"message": "funds placed",
                    "response": pmnt})

# Disburse funds
