import json


class BackendCmsRepositoryResponse:
    """
    Class responsible for wrapping responses from
    backend cms microservice
    """

    def __init__(self, is_success: bool, data):
        self.__is_success = is_success
        self.__data = data

    def get_data(self):
        """
        Method responsible for getting data from response
        """
        return self.__data if self.__data else {}

    def is_success(self):
        """
        Method responsible for checking does the request
        has finished with success
        """
        return self.__is_success

    def parse(self):
        try:
            return json.loads(self.__data)
        except Exception as ex:
            return {}


class BackendCmsCategoriesRepositoryResponse(BackendCmsRepositoryResponse):
    """
    Class responsible for wrapping response with categories
    form backend cms
    """

    # TODO: change names - not onyl categories

    def get_categories_descriptions(self) -> dict:
        return {key: value for key, value in self.get_data().items()}
