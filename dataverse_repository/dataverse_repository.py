import copy

import pysolr
from django.http import QueryDict
from pyDataverse.api import Api

from agregator_ofd.settings.common import DATAVERSE_URL, SOLR_COLLECTION_URL
from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from cache_manager.main import CacheManager, cached
from dataverse_client.dataverse_client import DataverseClient


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

    def __prepare_params(self, params: dict, search_type='datasets', exact=True) -> (
            str, dict):
        """
        Prepare proper params based on api client
        """
        q = "*"
        final_params = {'fq': ['publicationStatus:Published']}
        params = dict(
            copy.deepcopy(params).lists() if isinstance(params, QueryDict) else params)
        # ensure no facet fields sent
        if 'facet.field' in params:
            params.pop('facet.field')

        # ensure no publicationStatus will be changed
        if 'publicationStatus' in params:
            params.pop('publicationStatus')

        if 'dwcEventTime' in params:
            dwcEventTime = params['dwcEventTime']
            years = [year[:4] for year in dwcEventTime]
            final_params['fq'].append(f'dwcEventTime:{" TO ".join(years)}')
            params.pop('dwcEventTime')

        if 'timePeriodCovered' in params:
            time_period_covered = params['timePeriodCovered']
            years = [year[:4] for year in time_period_covered]
            final_params['fq'].append(f'timePeriodCovered:{" TO ".join(years)}')
            params.pop('timePeriodCovered')

        if 'geographicBoundingBox' in params:
            try:
                coords = [cord_value.split('_') for cord_value in
                          params['geographicBoundingBox']]
                # coords_dict = {
                #     'northLongitude': coords[1][0],
                #     'westLongitude': coords[0][1],
                #     'eastLongitude': coords[1][1],
                #     'southLongitude': coords[0][0]
                # }
                final_params['fq'].append(f'northLongitude:[* TO {coords[1][0]}]')
                final_params['fq'].append(f'westLongitude: [{coords[0][1]} TO *]')
                final_params['fq'].append(f'eastLongitude:[* TO {coords[1][1]}]')
                final_params['fq'].append(f'southLongitude: [{coords[0][0]} TO *]')
            except Exception as ex:
                print(ex)
                pass
            params.pop('geographicBoundingBox')

        if 'q' in params:
            q = params['q']
            params.pop('q')

        if 'rows' in params:
            final_params['rows'] = params['rows']
            params.pop('rows')

        if 'start' in params:
            final_params['start'] = [
                str(int(params['start'][0]) * (int(final_params['rows'][0]) or 15))]
            params.pop('start')

        if 'category' in params:
            params['identifierOfDataverse'] = params['category']
            params.pop('category')

        if 'sort' in params:
            if params['sort'] == ['asc']:
                final_params['sort'] = ['dateSort desc']
            else:
                final_params['sort'] = ['dateSort asc']
            params.pop('sort')
        else:
            final_params['sort'] = ['dateSort desc']

        media_static = params.get('mediaStatic', None)
        geo_static = params.get('geoStatic', None)
        if media_static:
            final_params['fq'].append(
                '{!join from=parentIdentifier to=identifier}fileContentType:image*')
            params.pop('mediaStatic')
        if geo_static:
            final_params['fq'].append('dwcDecimalLatitude:*')
            final_params['fq'].append('dwcDecimalLongitude:*')
            params.pop('geoStatic')

        params['dvObjectType'] = [search_type]

        for key, values in params.items():
            if isinstance(values, str):
                new_fquery = f'{key}:"{values}"'
            else:
                if exact:
                    new_fquery = f'{key}:' + " OR ".join(
                        [f'"{value}"' for value in values])
                else:
                    new_fquery = f'{key}:{" OR ".join([f"{value}" for value in values])}'
            final_params['fq'].append(new_fquery)
        return q, final_params

    def search(self, params: dict = None, facet_filterable_fields=[],
               search_type='datasets', exact=True) -> dict:
        """
        Prepare response with all required elements
        """
        # ensure params are in proper format
        query, params = self.__prepare_params(params, search_type=search_type,
                                              exact=exact)

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

        solr_response = self.__client.search("*", {
            'fq': ['dvObjectType:files', f'entityId:{resource_id}']})
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
            json_data = dataset.prepare_format()
            return json_data
        return None

    def get_datasets_details_based_on_identifier_list(self,
                                                      identifiers_list: list) -> dict:
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
            params={'fq': ["dvObjectType:dataverses"], 'start': ['0'], 'rows': ['100']})
        for dataverse in response_from_solr_search.get_result():
            categories.append({
                'id': dataverse['id'],
                'friendly_name': dataverse['name'],
                'name': dataverse['identifier'],
                'description': dataverse.get('description', ""),
                'dvName': dataverse.get('dvName', ""),
                'publicationDate': dataverse.get('publicationDate'),
                'dvAffiliation': dataverse.get('dvAffiliation')
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
                metadata_blocks[metadata_block[
                    'name']] = self.__client.get_metadata_details_for_block(
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

    def get_url_to_file(self, file_id: int, format=None) -> str:
        """
        Method responisble for getting api url
        to get - download file
        """
        if format:
            return f'{DATAVERSE_URL}/api/access/datafile/{file_id}?format={format}'
        return f'{DATAVERSE_URL}/api/access/datafile/{file_id}'

    def get_all_metrics_total(self, data_type, from_date, to_date):
        """
        Method responsible for obtaining all objects in datavers
        count from dataverse, also responsible for making all requests and
        join responses based on
        """
        response = self.__client.get_metrics(data_type, from_date, to_date)
        return response

    def get_metrics_total(self, data_type='dataverses', to_month=None, past_days=None):
        """
        Method responsible returning a count of various objects in dataverse over all-time:
        could be one of 4 types: dataverses, datasets, files or downloads
        """
        response = {}
        response_total_metrics = self.__client.get_metrics(data_type, to_month, past_days)
        if response_total_metrics.is_success:
            response['total'] = response_total_metrics.get_data()
        response_metrics_by_category = self.__client.get_metrics_by_category_of_dataverses()
        if response_metrics_by_category.is_success:
            response['datasets_category'] = response_metrics_by_category.get_data()
        response_metrics_by_subjects = self.__client.get_metrics_by_subject_of_datasets(
            to_month)
        if response_metrics_by_subjects.is_success:
            response['datasets_subject'] = response_metrics_by_subjects.get_data()
        return response or None

    def get_media_datasets(self, start=0, rows=15):
        """
        Method responsible for obtaining a list of datasets with medias in it
        """
        return self.__client.search('*', {'fq': ['publicationStatus:Published',
                                                 '{!join from=parentIdentifier to=identifier}fileContentType:image*',
                                                 'dvObjectType:datasets'], 'start': ['0'],
                                          'rows': ['31'],
                                          'sort': ['title asc']})

    def get_resource_download_times_amount(self, identifier: str):
        """
        Method responsible for getting amount of downloaded on each
        resource based on identifier
        """
        download_times = self.__client.dataset_download_amount(identifier)
        if download_times.is_success:
            return download_times.get_data()
        return {}
