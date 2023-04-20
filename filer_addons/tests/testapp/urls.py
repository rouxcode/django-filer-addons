from django.conf import settings
from django.urls import re_path
from django.contrib import admin
from django.conf.urls.static import static


admin.autodiscover()


urlpatterns = [
    re_path(
        r'^admin/',
        admin.site.urls
    ),
]


if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
