import requests
from pyDataverse.api import Api
import pysolr

from dataverse_client.dataverse_repository_response import DataverseClientResponse, \
    DataverseClientSearchResponse, DataverseDetailDatasetClientResponse
from dataverse_client.exceptions import DataverseClientConnectionException


class DataverseClient:
    """
    Repository pattern class to get each data from single dataverse instance
    """

    def __init__(self, client: Api, solr_client: pysolr.Solr):
        self.__dataverse_client = client
        self.__solr_client = solr_client
        self.check_connections()

    def check_connections(self) -> bool:
        """
        Checks connection of dataverse nad solr clients
        """
        if not self.__check_connections():
            raise DataverseClientConnectionException('Could not connect to Dataverse')
        return True

    def __check_connections(self) -> bool:
        """
        Method responsible for checking connection of each client used in repository
        """
        return True if self.__dataverse_client.status == 'OK' and self.__solr_client.verify else False

    def get_dataset_details(self, dataset_id: str) -> DataverseDetailDatasetClientResponse:
        """
        Method responsible for getting datased base on oid
        """
        return self.__get_dataset_details(dataset_id)

    def __get_dataset_details(self, identifier: str) -> DataverseDetailDatasetClientResponse:
        """
        Protected method responsible for obtaining dataset data
        based on identifier
        """
        response_from_dataverse = self.__dataverse_client.get_dataset(identifier)
        success = True if response_from_dataverse.status_code == requests.codes.ok else False
        return DataverseDetailDatasetClientResponse(success, response_from_dataverse.content)

    def __create_search_params(self, params: dict = None) -> dict:
        """
        Creates search params based on given dict with lists of strings as values
        Always basic search params should be provided as follow
        """
        search_query = {
            "fq": ["publicationStatus:Published"],
            'facet': ['on'],
            "facet.limit": ["-1"]
        }

        if params:
            # TODO this looks bad refactor needed - how to check if list is of strings?
            for key, search_params in params.items():
                if isinstance(search_params, list):
                    if key not in search_query:
                        search_query[key] = []
                    for search_param_value in search_params:
                        search_query[key].append(search_param_value)
        return search_query

    def search(self, phrase="*", params=None) -> DataverseClientSearchResponse:
        """
        Protected method responsible for obtaining searching results
        """
        try:
            response_from_dataverse = self.__solr_client.search(phrase, **self.__create_search_params(params))
            response = DataverseClientSearchResponse(True, response_from_dataverse)
        except Exception:
            # TODO: add exceptions for each type of error
            response = DataverseClientSearchResponse(False)
        return response
