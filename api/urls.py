from django.urls import path
from api import views as api_views

app_name = 'api'

urlpatterns = [
    # /api/v1/search
    path('search', api_views.SearchView.as_view(), name='search'),
    # /api/v1/structure
    path('structure', api_views.StructureView.as_view(), name='structure'),
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
    # /api/v1/available-metadata
    path('avilable-metadata', api_views.MetadataProvideView.as_view(), name='available_metadata'),
    # API CMS ENDPOINTS - BLOG, PAGES, CONTENT ETC...

    # /api/v1/pages
    path('home', api_views.HomeView.as_view(), name='cms_home_view'),
    path('pages', api_views.PageDetailsView.as_view(), name='cms_page_details'),
    path('blog', api_views.BlogListView.as_view(), name='cms_blog_index'),
    path('blog-slug', api_views.BlogDetails.as_view(), name='cms_blog_details'),
    path('news', api_views.NewsListView.as_view(), name='cms_news_index'),
    path('news-slug', api_views.NewsDetails.as_view(), name='cms_news_details'),
]
