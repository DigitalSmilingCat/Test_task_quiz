from django.urls import path
from .views import process_post_request


urlpatterns = [
    path('', process_post_request),
]