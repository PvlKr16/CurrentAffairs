from django.urls import path
from .views import create_topic, topic_detail, mark_unread, unread_count_api, unread_topics_page, search_topics

urlpatterns = [
    path('topic/new/', create_topic),
    path('topic/<int:topic_id>/', topic_detail),
    path('topic/<int:topic_id>/mark-unread/', mark_unread),
    path('api/unread-count/', unread_count_api),
    path('unread/', unread_topics_page),
    path('search/', search_topics),
]