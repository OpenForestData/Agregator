import json

from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from dataverse_repository.dataverse_repository import DataverseRepository


class DataConsistencyChecker:
    """
    Class responsible for periodic checking, and
    registering new data based on dataverse and backend_cms
    changes made by user
    """

    def __init__(self):
        self.__dataverse_repository = DataverseRepository()
        self.__backend_cms_repository = BackendCmsRepository()
        self.register_new_metadata_blocks()

    def register_new_metadata_blocks(self) -> bool:
        """
        Method responsible for registering metada blocks
        in backend cms based on dataverse response
        """
        dataverse_metadata_blocks = self.__dataverse_repository.get_all_metadata_blocks_details()
        return self.__backend_cms_repository.register_metadata_blocks(dataverse_metadata_blocks)

    def populate_categories(self) -> bool:
        """
        Method responsible for populating list of categories
        """
        categories_json = json.dumps({'categories':
                                          self.__dataverse_repository.get_all_categories()})
        return self.__backend_cms_repository.populate_categories(categories_json)
