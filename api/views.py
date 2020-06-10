from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from agregator_ofd.settings.common import DATASET_DETAILS_MAX_RESULTS_AMOUNT
from backend_cms_repository.backend_cms_repository import BackendCmsRepository
from dataverse_repository.dataverse_repository import DataverseRepository


class SearchView(APIView):
    """
    Basic view for search handling
    """
    permission_classes = ()

    def get(self, request):
        dataverse_repository = DataverseRepository()

        search_response = dataverse_repository.search(request.query_params)

        backend_cms_repository = BackendCmsRepository()
        backend_cms_repository.populate_categories_fields_list(dataverse_repository.get_all_categories())
        search_response['available_filter_fields']['category'] = backend_cms_repository.get_categories_fields_list()

        response = {
            'list': search_response,
            'global_data': backend_cms_repository.get_global_data()
        }
        return JsonResponse(response)


class DatasetDetailsView(APIView):
    permission_classes = ()

    def post(self, request):
        details_data = {}
        dataverse_repository = DataverseRepository()
        datasets_identifier_list = request.data.get('identifiers', None)
        if not datasets_identifier_list:
            return HttpResponse(content={'No identifiers supplied'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(datasets_identifier_list) > int(DATASET_DETAILS_MAX_RESULTS_AMOUNT):
            return HttpResponse(
                content={f'Too large datasets list. Max amount is {DATASET_DETAILS_MAX_RESULTS_AMOUNT}'},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        details_data = dataverse_repository.get_datasets_details_based_on_identifier_list(
            datasets_identifier_list)
        return JsonResponse(details_data)
