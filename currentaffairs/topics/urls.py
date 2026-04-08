from django.urls import path
from .views import create_topic

urlpatterns = [
    path('topic/new/', create_topic),
]