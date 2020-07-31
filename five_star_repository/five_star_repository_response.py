class FiveStarRepositoryResponse:
    """
    Class responsible for wrapping responses from
    five star repository microservice
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
