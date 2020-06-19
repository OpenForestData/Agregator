from django.urls import reverse

from agregator_ofd.settings.common import IMG_PROXY_THUMBNAILS_CREATION_MIME_TYPES
from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from dataverse_repository.dataverse_repository import DataverseRepository
from img_proxy_client.img_proxy_client import ImgProxyClient


# TODO add loggers


class AgregatorRepository:
    """
    Class responsible for preparing, joining and
    modifying data from repository and prepare them for each view
    """

    def __init__(self):
        self.__img_proxy_client = ImgProxyClient
        self.__dataverse_repository = DataverseRepository()
        self.__backend_cms_repository = BackendCmsRepository()

    def get_dataset(self, identifier: str) -> dict:
        dataset_data = self.__dataverse_repository.get_dataset_details(identifier)
        files_from_dataset = dataset_data.get('latestVersion', {}).get('files', None) if dataset_data else None
        if files_from_dataset:
            for file in files_from_dataset:
                data_file = file.get('dataFile', {})
                url_to_download_file = self.__dataverse_repository.get_url_to_file(
                    data_file.get('id', None))
                file['download_url'] = url_to_download_file
                # create thumbnail if mime type is correct
                if data_file.get(
                        'contentType', '') in IMG_PROXY_THUMBNAILS_CREATION_MIME_TYPES:
                    file['thumbnail_url'] = reverse('api:download_thumbnail',
                                                    kwargs={'file_id': data_file.get('id', None)})
        return dataset_data

    def get_datasets(self, identifiers_list: list) -> dict:
        """
        Method responsible for obtaining datasets information
        details
        """
        datasets = {}
        for identifier in identifiers_list:
            datasets[identifier] = self.get_dataset(identifier)
        return datasets

    def search(self, search_params: dict) -> dict:
        """
        Method responsible for handling search query, making query to
        dataverse and preparing data for right agregator format
        """
        facet_fields_data, basic_filter_fields_groups = self.__backend_cms_repository.get_facet_fields_list()
        filter_groups = {}
        facet_filterable_fields = {}
        # create dict based on names provided and divide for search and listing
        for group_name, value in facet_fields_data.items():
            for field in value['fields']:
                facet_filterable_fields[field['field_name']] = field
                filter_groups[group_name] = {'friendly_name': value['friendly_name'], 'id': value['id']}
        facet_filterable_fields_list = [key for key, _ in facet_filterable_fields.items()]

        response = self.__dataverse_repository.search(search_params, facet_filterable_fields_list)
        for key, value in response['listing_filter_fields'].items():
            value.update(facet_filterable_fields[key])
        categories = self.__backend_cms_repository.get_categories()
        # prepare basic filter fields for agregator listing view
        basic_filter_fields = {'category': categories}
        for group, value in basic_filter_fields_groups.items():
            for field in value['fields']:
                key = field['field_name']
                basic_filter_fields[key] = response['listing_filter_fields'][key]

        response['listing_filter_fields']['category'] = self.__backend_cms_repository.get_categories()
        response['filter_groups'] = filter_groups
        response['available_filter_fields'] = basic_filter_fields
        return {'list': response, 'global_data': self.__backend_cms_repository.get_global_data()}

    def get_reouserces(self, resources_ids: list) -> dict:
        """
        Method responsible for preparing response with
        metadata about resources based on their identifiers
        """
        # TODO wywalic wersje, nie robić
        # TODO dodajemy dataset na podstawie dataset
        response = {}
        for id in resources_ids:
            resource_details = self.__dataverse_repository.get_resource(id)
            if resource_details:
                url_to_download_file = self.__dataverse_repository.get_url_to_file(id)
                response['details'] = resource_details
                response['download_url'] = url_to_download_file
        return response

    def get_thumbnail_url(self, file_id: int) -> (str, str):
        """
        Method responsible for generating thumbnail url
        based on img proxy
        """
        url_to_download_file = self.__dataverse_repository.get_url_to_file(file_id)
        url_thumbnail = self.__img_proxy_client.create_thumbnail_url(url_to_download_file, 100,
                                                                     0)
        return url_thumbnail, str(file_id)
