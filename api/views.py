from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from agregator_ofd.settings.common import DATASET_DETAILS_MAX_RESULTS_AMOUNT
from agregator_repository.agregator_repository import AgregatorRepository
from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from data_consistency_checker.data_consistency_checker import DataConsistencyChecker
from dataverse_repository.dataverse_repository import DataverseRepository


class SearchView(APIView):
    """
    Basic view for search handling
    """
    permission_classes = ()

    def get(self, request):
        search_params = request.query_params
        response = AgregatorRepository().search(search_params)
        return JsonResponse(response)


class DatasetDetailsView(APIView):
    """
    View responsible for obtaining dataset details views
    """
    permission_classes = ()

    def post(self, request):
        """
        Method responsible for handling data and prepare
        them for agrefator repository
        """

        datasets_identifier_list = request.data.get('identifiers', None)
        if not datasets_identifier_list:
            return HttpResponse(content={'No identifiers supplied'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(datasets_identifier_list) > int(DATASET_DETAILS_MAX_RESULTS_AMOUNT):
            return HttpResponse(
                content={f'Too large dataset list. Max amount is {DATASET_DETAILS_MAX_RESULTS_AMOUNT}'},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        agregator_repository = AgregatorRepository()
        details_data = agregator_repository.get_datasets(datasets_identifier_list)
        return JsonResponse(details_data)


class ResourceView(APIView):
    """
    View responsible for obtaining information about resources
    """
    permission_classes = ()

    def get(self, request, identifier_id):
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_reouserces([identifier_id])
        return JsonResponse(response)


class UpdateConsistency(APIView):
    """
    Class responsible for on demand updating data in backend cms
    """

    def get(self, request):
        updater = DataConsistencyChecker()
        updater.populate_categories()
        updater.register_new_metadata_blocks()
        return HttpResponse('Updated')
