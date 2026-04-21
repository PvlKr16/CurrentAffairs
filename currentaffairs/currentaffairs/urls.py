from django.contrib import admin
from django.urls import path, include
from core.views import root_redirect, home_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', root_redirect),
    path('home/', home_view),

    path('', include('users.urls')),
    path('', include('topics.urls')),
    path('', include('comments.urls')),

    path('set-language/', set_language, name='set_language'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
