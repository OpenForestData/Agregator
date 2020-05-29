from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [

    # /api/v1/core/hello-world
    path('hello-world/', views.HelloView.as_view(), name='hello'),
]
