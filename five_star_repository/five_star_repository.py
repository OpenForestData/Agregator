import requests
from rest_framework import status

from agregator_ofd.settings.common import FIVE_STAR_REPOSITORY_URL
from five_star_repository.five_star_repository_response import FiveStarRepositoryResponse


class FiveStarRepository:
    """
    Class responsible handling all requests for dataverse api
    """

    def __init__(self):
        self.host = FIVE_STAR_REPOSITORY_URL

    def get_metrics(self, data_type: str, from_date: str, to_date: str):
        url = self.host + f"/api-five/v1/metrics?data-type={data_type}&from={from_date}&to={to_date}"
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return FiveStarRepositoryResponse(True, response.content)
        return FiveStarRepositoryResponse(False, None)
