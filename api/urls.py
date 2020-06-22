from django.urls import path

from core import views as core_views
from api import views as api_views

app_name = 'api'

urlpatterns = [
    # /api/v1/hello-world
    path('hello-world/', core_views.HelloView.as_view(), name='hello'),
    # /api/v1/search
    path('search', api_views.SearchView.as_view(), name='search'),
    # /api/v1/dataset/details-view
    path('dataset', api_views.DatasetDetailsView.as_view(), name='dataset'),
    # /api/v1/datasets/<str:dataset_id>
    path('datasets', api_views.DatasetsDetailsView.as_view(), name='datasets'),
    # /api/v1/resource/123456
    path('resource/<str:identifier_id>', api_views.ResourceView.as_view(), name='resource'),
    # /api/v1/update-consistency
    path('update-consistency', api_views.UpdateConsistency.as_view(), name='update_consistency'),
    # /api/v1/thumbnail/12
    path('thumbnail/<int:file_id>', api_views.DownloadThumbnail.as_view(), name='download_thumbnail'),

    # API CMS ENDPOINTS - BLOG, PAGES, CONTENT ETC...

    # /api/v1/cms/page-details/o-firmie/en
    path('cms/page-details/<str:slug>/<str:lang_code>', api_views.PageDetailsView.as_view(), name='cms_page_details')
]
