from django.urls import path
from core.views import home_json
from .views import (
    create_topic,
    topic_detail,
    mark_unread,
    unread_count_api,
    unread_topics_page,
    search_topics,
    create_poll,
    view_poll,
    vote_poll,
    poll_results_api,
    add_topic_participant,
    leave_topic,
    add_poll_participant,
    leave_poll,
    follow_topic,
    unfollow_topic,
)

urlpatterns = [
    path('topic/new/', create_topic),
    path('topic/<int:topic_id>/', topic_detail),
    path('topic/<int:topic_id>/mark-unread/', mark_unread),

    path('topic/<int:topic_id>/add-user/', add_topic_participant),
    path('topic/<int:topic_id>/leave/', leave_topic),

    path('api/unread-count/', unread_count_api),
    path('unread/', unread_topics_page),
    path('search/', search_topics),

    path('poll/new/', create_poll),
    path('poll/<int:poll_id>/', view_poll),
    path('poll/<int:poll_id>/vote/', vote_poll),
    path('poll/<int:poll_id>/results/', poll_results_api),

    path('poll/<int:poll_id>/add-user/', add_poll_participant),
    path('poll/<int:poll_id>/leave/', leave_poll),

    path('topic/<int:topic_id>/follow/', follow_topic),
    path('topic/<int:topic_id>/unfollow/', unfollow_topic),

    path('api/home/', home_json),
]
