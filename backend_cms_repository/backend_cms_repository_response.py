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
        return self.__data

    def is_success(self):
        """
        Method responsible for checking does the request
        has finished with success
        """
        return self.__is_success
