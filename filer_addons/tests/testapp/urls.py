from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static


admin.autodiscover()


urlpatterns = [
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
]


if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
