from django.urls import path
from .views import create_topic, topic_detail, mark_unread

urlpatterns = [
    path('topic/new/', create_topic),
    path('topic/<int:topic_id>/', topic_detail),
    path('topic/<int:topic_id>/mark-unread/', mark_unread),
]