"""_summary_
"""


def u_test_http_response(
    client, endpoint, data, expected, headers=None
):  # pylint: disable=redefined-outer-name
    """_summary_

    Args:
        client (_type_): _description_
        data (_type_): _description_
        expected (_type_): _description_
    """
    response = client.post(endpoint, json=data, headers=headers)
    data = response.get_json()
    expected_data = expected["body"]
    data_type = type(expected_data)
    assert response.status_code == expected["status_code"]
    assert isinstance(data, data_type)
    assert data == expected_data
