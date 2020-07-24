import json
import mimetypes

import requests
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from rest_framework import status
from rest_framework.views import APIView

from agregator_ofd.settings.common import DATASET_DETAILS_MAX_RESULTS_AMOUNT
from agregator_repository.agregator_repository import AgregatorRepository
from data_consistency_checker.data_consistency_checker import DataConsistencyChecker


class SearchView(APIView):
    """
    Basic view for search handling
    """
    permission_classes = ()

    def get(self, request):
        search_params = request.query_params
        response = AgregatorRepository().search(search_params)
        return JsonResponse(response)


class StructureView(APIView):
    """
    Basic view for structure cms handling
    """
    permission_classes = ()

    def get(self, request):
        response = AgregatorRepository().get_cms_structure()
        return JsonResponse(response)


class MetadataProvideView(APIView):
    """
    Basic view for providing all available metadata fields
    """
    permission_classes = ()

    def get(self, request):
        response = AgregatorRepository().get_metadata()
        return JsonResponse(response)


class DatasetsDetailsView(APIView):
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


class DatasetDetailsView(APIView):
    """
    View responsible for obtaining dataset details views
    """
    permission_classes = ()

    def get(self, request):
        """
        Method responsible for handling data and prepare
        them for agrefator repository
        """
        identifier = request.query_params.get('identifier', None)
        if not identifier:
            return HttpResponse('No identifier supplied', status=status.HTTP_406_NOT_ACCEPTABLE)

        agregator_repository = AgregatorRepository()
        details_data = agregator_repository.get_dataset(identifier)
        if not details_data:
            return HttpResponse('Dataset does not exist', status=status.HTTP_404_NOT_FOUND)
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


class DownloadThumbnail(APIView):
    """
    Class responsible for streaming files for users
    """

    def get(self, request, file_id: int):
        agregator_repository = AgregatorRepository()
        url, filename = agregator_repository.get_thumbnail_url(file_id)
        r = requests.get(url, stream=True)
        content_type = r.headers['Content-Type']
        response = StreamingHttpResponse(streaming_content=r)
        extension = mimetypes.guess_extension(content_type)
        response['Content-Disposition'] = f'attachement; filename="{file_id}{extension}"'
        response['Content-Type'] = content_type
        return response


class PageDetailsView(APIView):
    """
    Class responsible for getting cms page details
    """

    def get(self, request):
        slug = request.GET.get('slug', "/pl")
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_page_details(slug)
        if response:
            return JsonResponse(response, safe=False)
        return HttpResponse(status=status.HTTP_404_NOT_FOUND, content="Page does not exist")


class BlogListView(APIView):
    """
    Class responsible for getting cms page details
    """

    def get(self, request):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 6)
        keywords_slug = request.GET.get('keyword', None)
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_blog_list(page, limit, keywords_slug)
        return JsonResponse(json.loads(response))


class BlogDetails(APIView):
    """
    Class responsible for getting cms page details
    """

    def get(self, request):
        slug = request.GET.get('slug', "")
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_page_details(slug)
        return JsonResponse(response)


class HomeView(APIView):
    """
    Class responsible for returnign main page data
    """

    def get(self, request):
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_home()
        return JsonResponse(response)


class NewsListView(APIView):
    """
    Class responsible for getting cms page details
    """

    def get(self, request):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 6)
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_news_list(page, limit)
        return JsonResponse(json.loads(response))


class Faq(APIView):
    """
    Class responsible fro getting faq from csm
    """

    def get(self, request):
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_faq()
        return JsonResponse(json.loads(response), safe=False)


class NewsDetails(APIView):
    """
    Class responsible for getting cms page details
    """

    def get(self, request):
        slug = request.GET.get('slug', "")
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_page_details(slug)
        return JsonResponse(response)


class DatasetOfTheDay(APIView):
    """
    Class responsible for getting dataset of the day
    """

    def get(self, request):
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_dataset_of_the_day()
        return JsonResponse(response)


class Metrics(APIView):
    """
    Class responsible for getting metrics from dataverse
    to query params: to-mont : RRRR-MM, pst-days: 12
    """

    def get(self, request):
        data_type = request.query_params.get('data-type', None)
        from_date = request.query_params.get('from', None)
        to_date = request.query_params.get('to', None)
        agregator_repository = AgregatorRepository()
        response = agregator_repository.get_metrics_total(from_date, to_date, data_type)
        return JsonResponse(response)
