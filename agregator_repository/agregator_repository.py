from agregator_ofd.settings.common import IMG_PROXY_THUMBNAILS_CREATION_MIME_TYPES
from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from dataverse_repository.dataverse_repository import DataverseRepository
from img_proxy_client.img_proxy_client import ImgProxyClient


class AgregatorRepository:
    """
    Class responsible for preparing, joining and
    modifying data from repository and prepare them for each view
    """

    def __init__(self):
        self.__img_proxy_client = ImgProxyClient
        self.__dataverse_repository = DataverseRepository()
        self.__backend_cms_repository = BackendCmsRepository()

    def get_datasets(self, identifiers_list: list) -> dict:
        """
        Method responsible for obtaining dataset information and
        update it with thumbnail and download resource urls
        """

        details_data = self.__dataverse_repository.get_datasets_details_based_on_identifier_list(
            identifiers_list)
        for dataset_id, dataset_data in details_data.items():
            files_from_dataset = dataset_data.get('latestVersion', {}).get('files', None)
            for file in files_from_dataset:
                data_file = file.get('dataFile', {})
                url_to_download_file = self.__dataverse_repository.get_url_to_file(
                    data_file.get('id', None))
                file['download_url'] = url_to_download_file
                # create thumbnail if mime type is correct
                file['thumbnail_url'] = self.__img_proxy_client.create_thumbnail_url(url_to_download_file, 200,
                                                                                     200) if data_file.get(
                    'contentType') in IMG_PROXY_THUMBNAILS_CREATION_MIME_TYPES else None
        return details_data

    def search(self, search_params: dict) -> dict:
        """
        Method responsible for handling search query, making query to
        dataverse and preparing data for right agregator format
        """
        facet_fields_data = self.__backend_cms_repository.get_facet_fields_list()
        filter_groups = {}
        facet_filterable_fields = {}
        # create dict based on names provided and divide for search and listing
        for group_name, value in facet_fields_data.items():
            for field in value['fields']:
                facet_filterable_fields[field['field_name']] = field
                filter_groups[group_name] = {'friendly_name': value['friendly_name'], 'id': value['id']}
        facet_filterable_fields_list = [key for key, _ in facet_filterable_fields.items()]

        response = self.__dataverse_repository.search(search_params, facet_filterable_fields_list)
        for key, value in response['available_filter_fields'].items():
            value.update(facet_filterable_fields[key])

        backend_cms_repository = BackendCmsRepository()
        # TODO: take categories from backend cms!
        response['available_filter_fields']['category'] = self.__backend_cms_repository.get_categories()
        response['filter_groups'] = filter_groups
        response['listing_filter_fields'] = {"TODO": "Ustalić z danielem jak to chce"}
        response['global_data'] = backend_cms_repository.get_global_data()
        return response

    def get_reouserces(self, resources_ids: list) -> dict:
        """
        Method responsible for preparing response with
        metadata about resources based on their identifiers
        """
        response = self.__dataverse_repository.get_datafiles_metadata(resources_ids)
        return response
