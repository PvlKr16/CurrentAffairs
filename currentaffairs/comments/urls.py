from django.urls import path
from .views import add_comment

urlpatterns = [
    path('topic/<int:topic_id>/comment/', add_comment),
]
