import json

import requests

from agregator_ofd.settings.common import BACKEND_CMS_URL


class BackendCmsRepository:
    """
    Class responsible for communication with backend cms
    and obtaining all informations
    """

    def __init__(self):
        self.host = BACKEND_CMS_URL

    def get_facet_fields_list(self):
        """
        Method responsible for obtaining facet fields names
        """

        url = self.host + '/pl/cms-api/v1/facet-list'
        facet_list = requests.get(url)
        try:
            facet_list_json = json.loads(facet_list.text)
            return {field['facet_field_name']: field['facet_field_friendly_name'] for field in facet_list_json}
        except Exception:
            print("Did not get data form cms")
            return {}

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
        menu_data = requests.get(self.host + '/pl/cms-api/global-data')
        return {}

    def populate_categories_fields_list(self, categories_fields_list: list) -> list:
        """
        Method responsible for populating categories and obtain
        actual categories sets
        """
        populated_categories_list = []
        url = self.host + '/pl/cms-api/populate-categories-fields-list/'
        response = requests.post(url, data={'categories_fields_list': categories_fields_list})
        return []

    def get_categories_fields_list(self):
        url = self.host + '/pl/cms-api/get-categories-fields-list/'
        response = requests.get(url)
        return ""

    def register_metadata_blocks(self, metadata_blocs_list) -> bool:
        url = self.host + '/pl/cms-api/register-metadata-blocks'
        response = requests.post(url, data=metadata_blocs_list)
        return True if response.status_code == 200 else False
