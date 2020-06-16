import json


class DataverseClientResponse:
    """
    Class responsible for creating all responses from dataverse api
    """

    def __init__(self, success: bool = False, data=None):
        self.__is_success = success
        self.__dataverse_data = data

    @property
    def is_success(self):
        return self.__is_success

    @property
    def data(self):
        return self.__dataverse_data

    def get_data(self):
        try:
            data = json.loads(self.data.text)['data']
        except Exception as ex:
            # TODO: add exception handler
            data = {}
        return data


class DataverseClientSearchResponse(DataverseClientResponse):
    """
    Basic solr response search class, responsible for handling
    proper formatting of solr search response
    """

    @property
    def facets(self) -> dict:
        """
        Shows all facets from solr response
        """
        try:
            return self.data.facets
        except Exception:
            return {}

    @property
    def facet_fields_values(self) -> dict:
        """
        Property to return proper format of facet fields
        """
        facet_values_dict = {}
        if 'facet_fields' in self.facets:
            for field_name, list_of_values in self.facets['facet_fields'].items():
                facet_values_dict[field_name] = {
                    'attributes': [{
                        'name': list_of_values[0::2][i],
                        'amount': list_of_values[1::2][i]
                    } for i in range(0, len(list_of_values[0::2]))]
                }
        return facet_values_dict

    @property
    def result(self) -> list:
        """
        Show results of solr search request
        """
        try:
            return self.data.docs
        except Exception:
            return []


class DataverseDetailDatasetClientResponse(DataverseClientResponse):
    """
    Class responsible for handling dataverse dataset details format
    proper handling
    """

    @property
    def json_data(self):
        try:
            return json.loads(self.data)['data']
        except Exception:
            return {}


class DataverseDataFileMetadataResponse(DataverseClientResponse):
    """
    Class responsible for handling dataverse dataile details response
    """

    def get_data(self):
        try:
            return json.loads(self.data.text)
        except Exception:
            return {}
