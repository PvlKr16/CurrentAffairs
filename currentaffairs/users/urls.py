from django.urls import path
from .views import login_view, logout_view, contacts_page, profile_page, change_theme

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('contacts/', contacts_page),
    path('profile/<int:user_id>/', profile_page),
    path('change-theme/', change_theme),
]
