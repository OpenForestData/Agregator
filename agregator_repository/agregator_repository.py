from datetime import datetime

from django.http import QueryDict
from django.urls import reverse

from agregator_ofd.settings.common import IMG_PROXY_THUMBNAILS_CREATION_MIME_TYPES
from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from dataverse_repository.dataverse_repository import DataverseRepository
from img_proxy_client.main import ImgProxyClient


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
        query_dict = QueryDict('', mutable=True)
        query_dict.update()
        dataset_search_data = self.__dataverse_repository.search({'identifier': ["*" + identifier[4:]]}, exact=False)
        dataset_data = self.__dataverse_repository.get_dataset_details(identifier)
        files_from_dataset = dataset_data.get('latestVersion', {}).get('files', None) if dataset_data else None
        if files_from_dataset:
            for file in files_from_dataset:
                data_file = file.get('dataFile', {})
                if 'text/tab' in data_file.get('contentType', ""):
                    url_to_download_file = self.__dataverse_repository.get_url_to_file(
                        data_file.get('id', None), format='original')
                else:
                    url_to_download_file = self.__dataverse_repository.get_url_to_file(
                        data_file.get('id', None))
                file['download_url'] = url_to_download_file
                # create thumbnail if mime type is correct
                if data_file.get(
                        'contentType', 'wrongValueNotInKeys') in IMG_PROXY_THUMBNAILS_CREATION_MIME_TYPES:
                    file['thumbnail_url'] = reverse('api:download_thumbnail',
                                                    kwargs={'file_id': data_file.get('id', None)})

        if dataset_search_data:
            dataset_data['search_info'] = dataset_search_data
        dataset_data['download_times'] = self.__dataverse_repository.get_resource_download_times_amount(identifier)
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

    def search(self, search_params: dict, language: str) -> dict:
        """
        Method responsible for handling search query, making query to
        dataverse and preparing data for right agregator format
        """
        facet_fields_data, basic_filter_fields_groups = self.__backend_cms_repository.get_facet_fields_list(language)
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
        categories = self.__backend_cms_repository.get_categories(language)
        # prepare basic filter fields for agregator listing view
        basic_filter_fields = {'category': categories}
        for group, value in basic_filter_fields_groups.items():
            for field in value['fields']:
                key = field['field_name']
                data = response['listing_filter_fields'].get(key, None)
                # ensure map and datefield could also be in basic filters
                if data and data.get('attributes', None) or data and data.get('type') in ['MAP', 'DATERANGE', "TEXT",
                                                                                          "TEXTBOX"]:
                    basic_filter_fields[key] = data

        response['listing_filter_fields']['category'] = self.__backend_cms_repository.get_categories(language)
        response['filter_groups'] = filter_groups
        response['available_filter_fields'] = basic_filter_fields
        response['categories_descriptions'] = self.__backend_cms_repository.get_categories_descriptions(language)
        return {'list': response, 'global_data': self.__backend_cms_repository.get_global_data(language)}

    def get_reouserces(self, resources_ids: list) -> dict:
        """
        Method responsible for preparing response with
        metadata about resources based on their identifiers
        """
        response = {}
        for id in resources_ids:
            resource_details = self.__dataverse_repository.get_resource(id)
            if resource_details:
                if 'text/tab' in resource_details.get('fileContentType', ""):
                    url_to_download_file = self.__dataverse_repository.get_url_to_file(
                        resource_details.get('entityId', None), format='original')
                else:
                    url_to_download_file = self.__dataverse_repository.get_url_to_file(
                        resource_details.get('entityId', None))
                if resource_details['fileTypeDisplay'] == 'Unknown':
                    resource_details['fileTypeDisplay'] = resource_details['name'].split(".")[-1]
                response['details'] = resource_details
                dataset_details = self.__dataverse_repository.get_dataset_details(
                    resource_details['parentIdentifier'])
                response['dataset_details'] = dataset_details
                files = {str(file['dataFile']['id']): file['dataFile']['filename'] for file in
                         dataset_details['latestVersion']['files']}
                response['details']['originalFileFormat'] = files.get(id, "").split('.')[-1]
                # response['details']['originalFileFormat'] = files
                response['download_url'] = url_to_download_file
                response['download_times'] = self.__dataverse_repository.get_resource_download_times_amount(id)
        return response

    def get_thumbnail_url(self, file_id: int) -> (str, str):
        """
        Method responsible for generating thumbnail url
        based on img proxy
        """
        url_to_download_file = self.__dataverse_repository.get_url_to_file(file_id)
        url_thumbnail = self.__img_proxy_client.create_thumbnail_url(url_to_download_file, 100, 0)
        return url_thumbnail, str(file_id)

    def get_metadata(self):
        """
        Method responsbile for obtaining information about all metadata in dataverse
        """
        return self.__dataverse_repository.get_all_metadata_blocks_details()

    def get_page_details(self, slug: str, language: str) -> dict:
        """
        Method responsible for obtaining page details based on given slug
        """
        return self.__backend_cms_repository.get_page_details(slug, language)

    def get_blog_list(self, language, page, limit, keywords_slug) -> dict:
        """
        Method responsible for obtaining page details based on given slug
        """
        return self.__backend_cms_repository.get_blog_list(language, page, limit, keywords_slug)

    def get_blog_details(self, slug: str) -> dict:
        """
        Method responsible for obtaining page details based on given slug
        """
        return self.__backend_cms_repository.get_blog_details(slug)

    def get_cms_structure(self, language: str):
        """
        Method responsible for getting cms page structure
        """
        return self.__backend_cms_repository.get_menu(language)

    def get_home(self, language: str):
        """
        Method responsible for getting all data gor home view
        """
        return self.__backend_cms_repository.get_home(language)

    def get_news_list(self, language, page, limit) -> dict:
        """
        Method responsible for getting all latest news
        """
        return self.__backend_cms_repository.get_news_list(language, page, limit)

    def get_dataset_of_the_day(self):
        """
        Method responsible for getting dataset of the day
        """
        media_datasets = self.__dataverse_repository.get_media_datasets()

        # If there aren't enough datasets with images, loop over dataset list from the start
        dataset_index = datetime.now().day % media_datasets.get_number_of_results()

        dataset_of_the_day = media_datasets.data.docs[dataset_index]
        return self.get_dataset(dataset_of_the_day['identifier'])

    def get_metrics_total(self, from_date, to_date, data_type):
        """
        Method responsible for getting metrics for specified data type
        """
        return self.__dataverse_repository.get_all_metrics_total(data_type, from_date, to_date)

    def get_faq(self, language: str):
        return self.__backend_cms_repository.get_faq(language)
