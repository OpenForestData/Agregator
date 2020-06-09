from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

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
        details_data = dataverse_repository.get_datasets_details_based_on_identifier_list(
            [result['identifier'] for result in search_response['results']])
        for result in search_response['results']:
            result['details'] = details_data[result['identifier']]
        search_response['available_filter_fields']['category'] = dataverse_repository.get_all_categories()
        backend_cms_repository = BackendCmsRepository()
        response = {
            'list': search_response,
            'global_data': backend_cms_repository.get_global_data()
        }
        return JsonResponse(response)
