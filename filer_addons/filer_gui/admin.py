from __future__ import unicode_literals

from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.http.response import JsonResponse

from .models import File, FilerGuiFile
from .widgets import THUMBNAIL_SIZE  # TODO get it from settings


class FilerGuiFileSelectForm(forms.Form):
    filer_file = forms.ModelChoiceField(
        queryset=File.objects.all()
    )


@admin.register(FilerGuiFile)
class FilerGuiAdmin(admin.ModelAdmin):
    original_model = File

    def get_urls(self):
        urls = [
            url(
                r'^file-detail-json/$',
                self.admin_site.admin_view(self.file_detail_json_view),
                name='file_detail_json_for_id'
            ),
        ]
        return urls

    def file_detail_json_view(self, request):
        form = FilerGuiFileSelectForm(request.POST)
        if form.is_valid():
            obj = form.cleaned_data.get('filer_file')
            if obj.file_type == 'Image':
                th = obj.easy_thumbnails_thumbnailer
                thumb = th.get_thumbnail({'size': THUMBNAIL_SIZE})
                thumb_url = thumb.url
            else:
                thumb_url = obj.icons['48']
            data = {
                'message': 'ok',
                'file': {
                    'thumb_url': thumb_url,
                    'file_url': obj.url,
                    'label': obj.label
                },
            }
        else:
            data = {
                'message': 'error',
                'error': 'no valid file id',
            }
        return JsonResponse(data=data)

    def get_thumbnail(self, obj, size=None):
        size = size or THUMBNAIL_SIZE

    def get_model_perms(self, *args, **kwargs):
        """
        It seems this is the only way to hide this admin in the app_index :(
        """
        return {
            'add': False,
            'change': False,
            'delete': False,
        }
