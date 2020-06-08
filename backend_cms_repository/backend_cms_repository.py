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
        facet_list = requests.get(self.host + '/pl/cms-api/v1/facet-list')
        try:
            facet_list_json = json.loads(facet_list.text)
            return {field['facet_field_name']: field['facet_field_friendly_name'] for field in facet_list_json}
        except Exception:
            return []

    def get_global_data(self) -> dict:
        """
        Method responsible for obtaining data that are repeated in
        each view of a agregator (menus, analytics, etc)
        """
        return {}

    def get_menu(self) -> dict:
        menu_data = requests.get(self.host + '/pl/cms-api/global-data')
        return {}
