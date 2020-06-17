import json

import requests
from rest_framework import status

from agregator_ofd.settings.common import BACKEND_CMS_URL

# TODO add loggers
from cache_manager.cache_manager import cached


class BackendCmsRepository:
    """
    Class responsible for communication with backend cms
    and obtaining all informations
    """

    def __init__(self):
        self.host = BACKEND_CMS_URL

    @cached
    def get_facet_fields_list(self):
        """
        Method responsible for obtaining facet fields names
        """
        url = self.host + '/cms-api/v1/facet-list'
        response = requests.get(url)
        if response.status_code != status.HTTP_200_OK:
            return {}
        facet_list = json.loads(response.text)
        return facet_list

    def get_global_data(self) -> dict:
        """
        Method responsible for obtaining data that are repeated in
        each view of a agregator (menus, analytics, etc)
        """
        return {}

    def get_menu(self) -> dict:
        """
        Method responsible for getting menu structure
        """
        menu_data = requests.get(self.host + '/cms-api/v1/global-data')
        return {}

    def populate_categories(self, categories_json: str) -> bool:
        """
        Method responsible for populating categories and obtain
        actual categories sets
        """
        url = self.host + '/cms-api/v1/populate-categories-fields-list'
        response = requests.post(url, data={'categories_fields_list': categories_json})
        return response.status_code == status.HTTP_200_OK

    @cached
    def get_categories(self):
        url = self.host + '/cms-api/v1/get-categories'
        categories_list_json = requests.get(url)
        try:
            facet_list = json.loads(categories_list_json.text)
            return facet_list
        except Exception:
            print("Did not get data from cms")
            return {}
        # TODO exception out

    def register_metadata_blocks(self, metadata_blocks_list) -> bool:
        url = self.host + '/cms-api/v1/register-metadata-blocks'
        response = requests.post(url, data={'metadata_blocks': json.dumps(metadata_blocks_list)})
        return response.status_code == status.HTTP_200_OK
