"""_summary_
"""
from tests.unit import app, client  # pylint: disable=unused-import


def test_user_registration_ok(client):
    """_summary_

    Args:
        client (_type_): _description_
    """
    data = {
        "name": "Jimena Lopez",
        "username": "jimenalogo",
        "email": "jimenalogo@gmail.com",
        "mobile": "+573046628057",
        "password": "secret",
    }
    response = client.post("/v1/users", json=data)
    assert response.status_code == 201
