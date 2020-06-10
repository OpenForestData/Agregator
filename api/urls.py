from django.urls import path

from core import views as core_views
from api import views as api_views

app_name = 'api'

urlpatterns = [

    # /api/v1/hello-world
    path('hello-world/', core_views.HelloView.as_view(), name='hello'),
    # /api/v1/search
    path('search', api_views.SearchView.as_view(), name='search'),
    # /api/v1/datasets/details-view
    path('datasets', api_views.DatasetDetailsView.as_view(), name='datasets'),
]
