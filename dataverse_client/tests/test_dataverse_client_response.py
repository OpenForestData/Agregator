import json
import pytest

from requests.models import Response
from pysolr import Results

from dataverse_client.dataverse_client_response import DataverseClientResponse, \
    DataverseClientSearchResponse, DataverseDetailDatasetClientResponse, DataverseDataFileMetadataResponse


def create_response(data):
    """
    Creates request response based on given data
    """
    response = Response()
    response._content = str.encode(data)
    return response


def create_ddcr_with_author(author):
    field = {'typeName': 'author', 'value': author}
    return {'data': {'latestVersion': {'metadataBlocks': {'citation': {'fields': [field]}}}}}


def create_ddcr_with_url(url):
    field = {'typeName': 'alternativeURL', 'value': url}
    return {'data': {'latestVersion': {'metadataBlocks': {'citation': {'fields': [field]}}}}}


@pytest.mark.parametrize(
    'is_success', [True, False]
)
def test_response_is_success(is_success):
    """
    Tests checking does the request has finished with success
    """
    response = DataverseClientResponse(is_success, {'type': 'tests'})
    assert response.is_success == is_success


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_response_data(data):
    """
    Tests wrapped request data, when request has finished with success
    """
    response = DataverseClientResponse(True, data)
    assert response.data == data


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_response_get_with_data(data):
    """
    Tests loading json with data field
    """
    result = create_response(json.dumps({'data': data}))
    response = DataverseClientResponse(True, result)
    assert response.get_data() == data


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_response_get_without_data(data):
    """
    Tests loading json without data field
    """
    result = create_response(json.dumps(data))
    response = DataverseClientResponse(True, result)
    assert response.get_data() == {}


def test_dcs_response():
    """
    Tests DataverseClientSearchResponse with valid response
    """
    facet = {
        'facet_fields': {
            "gender": ["Men", 25, "Women", 0],
            "style": ["casual", 0.5, "dress", 0.2]
        }
    }
    facet_value = {
        "gender": {
            "attributes": [{"name": "Men", "amount": 25}, {"name": "Women", "amount": 0}]
        },
        "style": {
            "attributes": [{"name": "casual", "amount": 0.5}, {"name": "dress", "amount": 0.2}]
        }
    }
    docs = [{'id': 1}, {'id': 2}, {'id': 3}]
    number = 5
    raw = {
        'response': {'numFound': number, 'docs': docs},
        'facet_counts': facet
    }
    data = Results(raw)
    response = DataverseClientSearchResponse(True, data)
    assert response.get_facets() == facet
    assert response.get_result() == docs
    assert response.get_number_of_results() == number
    assert response.get_facet_fields_values() == facet_value


@pytest.mark.parametrize(
    'data', [Results({}), None]
)
def test_dcs_response_empty(data):
    """
    Tests DataverseClientSearchResponse with empty response and non response
    """
    response = DataverseClientSearchResponse(True, data)
    assert response.get_facets() == {}
    assert response.get_result() == []
    assert response.get_number_of_results() == 0
    assert response.get_facet_fields_values() == {}


@pytest.mark.parametrize(
    'author', [{}, None, True, 'John', 12, ['Jim', 'John', 'Steve']]
)
def test_ddc_response_prepare_author(author):
    """
    Tests preparing author format
    """
    data = json.dumps(create_ddcr_with_author(author))
    response = DataverseDetailDatasetClientResponse(True, data)
    result = response.prepare_format()
    assert result['providers'] == author
    assert result['alternativeURL'] == ""


@pytest.mark.parametrize(
    'url', [{}, None, True, 'John', 12, ['Jim', 'John', 'Steve']]
)
def test_ddc_response_prepare_url(url):
    """
    Tests preparing alternative url format
    """
    data = json.dumps(create_ddcr_with_url(url))
    response = DataverseDetailDatasetClientResponse(True, data)
    result = response.prepare_format()
    assert result['providers'] == []
    assert result['alternativeURL'] == url


def test_ddc_response_prepare_empty():
    """
    Tests preparing format of empty data
    """
    data = json.dumps(None)
    response = DataverseDetailDatasetClientResponse(True, data)
    result = response.prepare_format()
    assert result['providers'] == []
    assert result['alternativeURL'] == ""


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_dfm_response_get_with_json(data):
    """
    Tests loading content of dataverse reponse with json encoding
    """
    result = create_response(json.dumps(data))
    response = DataverseDataFileMetadataResponse(True, result)
    assert response.get_data() == data


@pytest.mark.parametrize(
    'data', [1, -0.5, 'data', [1, 2, 3], None, False, {'id': 1, 'name': 'Janek', 'male': False}]
)
def test_dfm_response_get_without_json(data):
    """
    Tests loading content of dataverse reponse without json encoding
    """
    result = str(data)
    response = DataverseDataFileMetadataResponse(True, result)
    assert response.get_data() == {}
