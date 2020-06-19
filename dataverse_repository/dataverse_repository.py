import json

import pysolr
from pyDataverse.api import Api

from agregator_ofd.settings.common import DATAVERSE_URL, SOLR_COLLECTION_URL
from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from cache_manager.cache_manager import CacheManager, cached
from dataverse_client.dataverse_client import DataverseClient


# TODO add loggers


class DataverseRepository:
    """
    Class responsible handling all requests for dataverse api
    """

    def __init__(self):
        self.__client = DataverseClient(Api(DATAVERSE_URL),
                                        pysolr.Solr(SOLR_COLLECTION_URL))
        self.__backend_cms_repository = BackendCmsRepository()
        # TODO delete backend_cms repository
        self.__cache = CacheManager()

    def __prepare_params(self, params: dict, search_type='datasets') -> (str, dict):
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

        if 'mediaTypeStatic' in params:
            if params['mediaTypeStatic'] == 'image':
                params['advanced_query'] = ['{!join from=parentIdentifier to=identifier}fileContentType:image*']
            if params['mediaTypeStatic'] == 'geonode':
                params['westLongitude'] = ["*"]
            params.pop('mediaTypeStatic')

        params['dvObjectType'] = [search_type]

        for key, values in params.items():
            new_fquery = f"{key}:{' OR '.join([value for value in values])}"
            final_params['fq'].append(new_fquery)
        return q, final_params

    def search(self, params: dict = None, facet_filterable_fields=[], search_type='datasets') -> dict:
        """
        Prepare response with all required elements for response
        """
        # ensure params are in proper format
        query, params = self.__prepare_params(params, search_type=search_type)
        # TODO get out as param facet_fields_list
        # get search params from backend cms
        search_params = {'facet.field': facet_filterable_fields}

        # update query based on data sent by front
        search_params.update(**params)
        response = {}
        dataverse_client_response = self.__client.search(query, search_params)
        facet_fields_values = dataverse_client_response.get_facet_fields_values()
        response['listing_filter_fields'] = facet_fields_values
        response['results'] = dataverse_client_response.get_result()
        response['amount'] = dataverse_client_response.get_number_of_results()
        return response

    @cached
    def get_resource(self, resource_id: str):
        solr_response = self.__client.search("*", {'fq': ['dvObjectType:files', f'entityId:{resource_id}']})
        resource = solr_response.get_result()
        if len(resource) > 0:
            return resource[0]
        return None

    @cached
    def get_dataset_details(self, identifier: str):
        """
        Method responsible for getting dataset details (uses dataverse api client)
        """
        dataset = self.__client.get_dataset_details(identifier)
        if dataset.is_success:
            json_data = dataset.get_json_data()
            return json_data
        return None

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
        for dataverse in response_from_solr_search.get_result():
            categories.append({
                'id': dataverse['id'],
                'friendly_name': dataverse['name'],
                'name': dataverse['identifier'],
            })
        return categories

    def get_all_metadata_blocks_details(self) -> dict:
        """
        Method to get full list of metadata blocks and their attributes
        """
        metadata_blocks = {}
        metadata_blocks_response = self.__client.get_metadata_blocks()
        if metadata_blocks_response.is_success:
            all_metadata_blocks = metadata_blocks_response.get_data()
            for metadata_block in all_metadata_blocks:
                metadata_blocks[metadata_block['name']] = self.__client.get_metadata_details_for_block(
                    metadata_block['name']).get_data()
        return metadata_blocks

    @cached
    def get_datafile_metadata(self, identifier_id: str) -> dict:
        """
        Method responsible for obtaining datafile metada
        based on identifier
        """
        response = self.__client.get_datafile_metadata(identifier_id)
        if response.is_success:
            data = response.get_data()
        else:
            data = {}
        return data

    def get_datafiles_metadata(self, identifiers_list: list) -> dict:
        """
        Method responsible for obtaining metadata for
        many datafiles based on list of identifiers
        """
        data = {}
        for identifier in identifiers_list:
            data[identifier] = self.get_datafile_metadata(identifier)
        return data

    def get_url_to_file(self, file_id: int) -> str:
        """
        Method responisble for getting api url
        to get - download file
        """
        return f'{DATAVERSE_URL}/api/access/datafile/{file_id}'
