from django.urls import path

from .views import get_content_list


urlpatterns = [
    path('contents', get_content_list, name='get_content_list'),
]