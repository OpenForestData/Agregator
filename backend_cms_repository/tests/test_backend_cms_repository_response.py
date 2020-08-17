import json
import pytest

from backend_cms_repository.backend_cms_repository_response import BackendCmsRepositoryResponse


@pytest.mark.parametrize(
    'is_success', [True, False]
)
def test_response_is_success(is_success):
    """
    Tests checking does the request has finished with success
    """
    response = BackendCmsRepositoryResponse(is_success, {'type': 'tests'})
    assert response.is_success() == is_success


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_response_data(data):
    """
    Tests wrapped request data, when request has finished with success
    """
    response = BackendCmsRepositoryResponse(True, data)
    assert response.get_data() == data


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_response_data_no_success(data):
    """
    Tests wrapped request data, when request has finished without success
    """
    response = BackendCmsRepositoryResponse(False, data)
    assert response.get_data() == {}


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_response_parse_json(data):
    """
    Tests loading json with parser
    """
    json_string = json.dumps(data)
    response = BackendCmsRepositoryResponse(True, json_string)
    assert response.parse() == data


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_response_parse_data(data):
    """
    Tests loading data with parser
    """
    response = BackendCmsRepositoryResponse(True, data)
    assert response.parse() == {}
