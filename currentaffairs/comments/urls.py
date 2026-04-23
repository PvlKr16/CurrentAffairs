from django.urls import path
from .views import add_comment, comments_json

urlpatterns = [
    path('topic/<int:topic_id>/comment/', add_comment),
    path('topic/<int:topic_id>/comments-json/', comments_json),
]
