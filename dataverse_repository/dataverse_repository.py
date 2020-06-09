import pysolr
from pyDataverse.api import Api

from agregator_ofd.settings.common import DATAVERSE_URL, SOLR_COLLECTION_URL
from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from dataverse_client.dataverse_client import DataverseClient


class DataverseRepository:
    """
    Class responsible handling all requests for dataverse api
    """

    def __init__(self):
        self.__client = DataverseClient(Api(DATAVERSE_URL),
                                        pysolr.Solr(SOLR_COLLECTION_URL))
        # TODO should be as param, when redis will be available
        self.__backend_cms_repository = BackendCmsRepository()

    def __prepare_params(self, params: dict) -> (str, dict):
        """
        Prepare proper params based on api client
        """
        q = "*"
        final_params = {'fq': []}
        params = params.copy()
        # ensure no facet fields sent
        if 'facet.field' in params:
            params.pop('facet.field')

        # ensure no publicationStatus will be changed
        if 'publicationStatus' in params:
            params.pop('publicationStatus')

        if 'q' in params:
            q = params['q']
            params.pop('q')

        if 'start' in params:
            final_params['start'] = [params['start']]
            params.pop('start')

        if 'rows' in params:
            final_params['rows'] = [params['rows']]
            params.pop('rows')

        if 'category' in params:
            params['identifierOfDataverse'] = params['category']
            params.pop('category')

        for key, values in params.items():
            new_fquery = f"{key}:{' OR '.join([value for value in params.getlist(key)])}"
            final_params['fq'].append(new_fquery)
        return q, final_params

    def search(self, params: dict = None) -> dict:
        """
        Prepare response with all required elements for response
        """
        # ensure params are in proper format
        query, params = self.__prepare_params(params)
        facet_fields_data = self.__backend_cms_repository.get_facet_fields_list()
        # get search params from backend cms
        search_params = {'facet.field': list(facet_fields_data.keys())}
        # update query based on data send by front
        search_params.update(**params)
        response = {}
        dataverse_client_response = self.__client.search(query, search_params)
        facet_fields_values = dataverse_client_response.facet_fields_values
        for key, value in facet_fields_values.items():
            value['friendly_name'] = facet_fields_data[key]
        response['available_filter_fields'] = facet_fields_values
        response['results'] = dataverse_client_response.result
        return response

    def get_dataset_details(self, identifier: str) -> dict:
        """
        Method responsible for getting dataset details (uses dataverse api client)
        """
        return self.__client.get_dataset_details(identifier).json_data

    def get_datasets_details_based_on_identifier_list(self, identifiers_list: list) -> dict:
        """
        Method responsible for getting dataset details for search
        """
        response = {}
        for identifier in identifiers_list:
            response[identifier] = self.get_dataset_details(identifier)
        return response

    def get_all_categories(self) -> list:
        """
        Method responsible for getting all dataverses - treated as categories
        in agregator based on solr searh query
        """
        categories = []
        response_from_solr_search = self.__client.search(
            params={'fq': ["dvObjectType:dataverses"], 'start': ['1'], 'rows': ['15']})
        for dataverse in response_from_solr_search.result:
            categories.append({
                'id': dataverse['id'],
                'friendly_name': dataverse['name'],
                'name': dataverse['identifier'],
            })
        return categories
