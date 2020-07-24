import json

import requests
from rest_framework import status

from agregator_ofd.settings.common import BACKEND_CMS_URL
from backend_cms_repository.backend_cms_repository_response import BackendCmsRepositoryResponse, \
    BackendCmsCategoriesRepositoryResponse


class BackendCmsClient:
    """
    Class responsible for getting information from each endpoint
    of backend cms repository
    """

    def __init__(self):
        self.host = BACKEND_CMS_URL

    def get_facet_fields(self):
        """
        Method responsible for obtaining facet fields
        from backend cms
        """
        url = self.host + '/cms-api/v1/facet-list'
        response = requests.get(url)
        if response.status_code != status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(False, None)
        try:
            parsed_data = json.loads(response.text)
        except Exception as ex:
            print(ex)
            parsed_data = None
        return BackendCmsRepositoryResponse(True, parsed_data)

    def get_menu(self):
        """
        Method responsible for geting menu nodes
        from backend cms
        """
        response = requests.get(self.host + '/cms-api/v1/menu')
        if response.status_code != status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(False, None)
        try:
            parsed_data = json.loads(response.text)
        except Exception as ex:
            print(ex)
            parsed_data = None
        return BackendCmsRepositoryResponse(True, parsed_data)

    def get_page_details(self, slug: str) -> BackendCmsRepositoryResponse:
        """
        Method responsible for getting page details from backend cms
        """
        response = requests.get(self.host + slug)
        if response.status_code != status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(False, None)
        try:
            parsed_data = json.loads(response.text)
        except Exception as ex:
            print(ex)
            parsed_data = None
        return BackendCmsRepositoryResponse(True, parsed_data)

    def get_categories(self) -> BackendCmsCategoriesRepositoryResponse:
        """
        Method responsible for getting categories in proper order
        from backend cms
        """
        url = self.host + '/cms-api/v1/get-categories'
        response = requests.get(url)
        if response.status_code != status.HTTP_200_OK:
            return BackendCmsCategoriesRepositoryResponse(False, None)
        try:
            parsed_data = json.loads(response.text)
        except Exception as ex:
            print(ex)
            parsed_data = None
        return BackendCmsCategoriesRepositoryResponse(True, parsed_data)

    def populate_categories(self, categories_json):
        """
        Method responsible for populating categories
        from dataverse (dataverses) in backend cms
        """
        url = self.host + '/cms-api/v1/populate-categories-fields-list'
        response = requests.post(url, data={'categories_fields_list': categories_json})
        if response.status_code == status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(True, None)
        return BackendCmsRepositoryResponse(False, None)

    def register_metadata_blocks(self, metadata_blocks_list):
        """
        Method responsible for registering metadata blocks
        from dataverse in backend cms
        """
        url = self.host + '/cms-api/v1/register-metadata-blocks'
        response = requests.post(url, data={'metadata_blocks': json.dumps(metadata_blocks_list)})
        if response.status_code == status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(True, None)
        return BackendCmsRepositoryResponse(False, None)

    def get_blog_index(self, page=1, limit=6, keywords_slug=None):
        """
        Method responsible for obtaining blog index page
        """
        url = self.host + f'/cms-api/v1/blog/index?page={page}&limit={limit}'
        if keywords_slug:
            url += f'&keyword={keywords_slug}'
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(True, response.text)
        return BackendCmsRepositoryResponse(False, None)

    def get_news_index(self, page=1, limit=6):
        """
        Method responsible for obtaining news index page
        """
        url = self.host + f'/cms-api/v1/news/latest?page={page}&limit={limit}'
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(True, response.text)
        return BackendCmsRepositoryResponse(False, None)

    def get_blog_details(self, slug):
        """
        Method responsible for obtaining blog details about
        article
        """
        url = self.host + slug
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(True, response.text)
        return BackendCmsRepositoryResponse(False, None)

    def get_blog_keyword_list(self, slug):
        """
        Method responsible for obtaining blog keyword articles list
        """
        url = self.host + slug
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(True, response.text)
        return BackendCmsRepositoryResponse(False, None)

    def get_home(self):
        """
        Method responsible for getting all main page (home) informations
        """
        url = self.host + '/cms-api/v1/home'
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(True, response.text)
        return BackendCmsRepositoryResponse(False, None)

    def get_faq(self):
        """
        Method responsible for getting all faqs informations
        """
        url = self.host + '/cms-api/v1/faq'
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return BackendCmsRepositoryResponse(True, response.text)
        return BackendCmsRepositoryResponse(False, None)