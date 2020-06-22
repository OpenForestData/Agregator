import json

import requests
from rest_framework import status

from agregator_ofd.settings.common import BACKEND_CMS_URL

# TODO add loggers
from backend_cms_repository.backend_cms_client import BackendCmsClient
from cache_manager.cache_manager import cached


class BackendCmsRepository:
    """
    Class responsible for communication with backend cms
    and obtaining all informations
    """

    def __init__(self):
        self.__client = BackendCmsClient()
        self.get_menu()

    @cached
    def get_facet_fields_list(self) -> (dict, dict):
        """
        Method responsible for obtaining facet fields names
        """
        facet_list = self.__client.get_facet_fields().get_data()
        advanced_search_list = {}
        basic_filters = {}
        if 'advanced_search_filters' in facet_list:
            advanced_search_list = facet_list['advanced_search_filters']

        if 'basic_filters' in facet_list:
            basic_filters = facet_list['basic_filters']
        return advanced_search_list, basic_filters

    def get_global_data(self) -> dict:
        """
        Method responsible for obtaining data that are repeated in
        each view of a agregator (menus, analytics, etc)
        """
        return {}

    @cached
    def get_menu(self) -> dict:
        """
        Method responsible for getting menu structure
        """
        menu_response = self.__client.get_menu()
        if menu_response.is_success():
            return menu_response.get_data()
        return {}

    def get_page(self, id) -> dict:
        """
        Method responsible for obtaining all single
        page data
        """
        page_response = self.__client.get_page_details(id)
        return {}

    def populate_categories(self, categories_json: str) -> bool:
        """
        Method responsible for populating categories and obtain
        actual categories sets
        """
        response = self.__client.populate_categories(categories_json)
        return response.is_success()

    @cached
    def get_categories(self):
        categories = self.__client.get_categories()
        if categories.is_success():
            return categories.get_data()
        return {}

    def register_metadata_blocks(self, metadata_blocks_list) -> bool:
        """
        Method responsible for registering metadata blocks in backend cms
        """
        return self.__client.register_metadata_blocks(metadata_blocks_list).is_success()
