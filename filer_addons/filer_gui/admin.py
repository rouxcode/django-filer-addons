from __future__ import unicode_literals

from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.http.response import JsonResponse

from .models import File, Image, FilerGuiFile
# TODO get it from settings
from .widgets import FILE_TYPE_CHOICES, THUMBNAIL_SIZE


class FilerGuiFileSelectForm(forms.Form):
    """
    Simple form to check if file exists
    """
    filer_file = forms.ModelChoiceField(
        queryset=File.objects.all()
    )


class FilerGuiUploadForm(forms.Form):
    """
    Simple form to check if the upload is ok
    """
    file = forms.FileField()
    file_type = forms.ChoiceField(
        choices=FILE_TYPE_CHOICES,
        initial=FILE_TYPE_CHOICES[0][0]
    )


class FilerFileForm(forms.ModelForm):
    """
    Simple form to create a filer file
    """

    class Meta:
        model = File
        fields = [
            'file',
            'is_public',
            'original_filename',
            'owner',
        ]


class FilerImageForm(forms.ModelForm):
    """
    Simple form to create a filer file
    """

    class Meta:
        model = Image
        fields = [
            'file',
            'is_public',
            'original_filename',
            'owner',
        ]


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
            url(
                r'^file-upload/$',
                self.admin_site.admin_view(self.file_upload_view),
                name='file_upload'
            ),
        ]
        return urls

    def get_file_detail_dict(self, obj):
        if obj.file_type == 'Image':
            th = obj.easy_thumbnails_thumbnailer
            thumb = th.get_thumbnail({'size': THUMBNAIL_SIZE})
            thumb_url = thumb.url
        else:
            thumb_url = obj.icons['48']
        data = {
            'label': obj.label,
            'file_id': obj.id,
            'file_url': obj.url,
            'icon_url': obj.icons['48'],
            'thumb_url': thumb_url,
        }
        return data

    def file_detail_json_view(self, request):
        form = FilerGuiFileSelectForm(request.POST)
        if form.is_valid():
            obj = form.cleaned_data.get('filer_file')
            data = {
                'message': 'ok',
                'file': self.get_file_detail_dict(obj),
            }
        else:
            data = {
                'message': 'error',
                'error': 'no valid file id',
            }
        return JsonResponse(data=data)

    def file_upload_view(self, request):
        data = {}
        files = getattr(request, 'FILES')
        if not files:
            data = {
                'message': 'error',
                'error': 'no file'
            }
        else:
            form = FilerGuiUploadForm(request.POST, request.FILES)
            if form.is_valid():
                # TODO get rid of this distinction
                # FIXME Check how divio does that and adapt it.
                if form.cleaned_data['file_type'].lower() == 'image':
                    form_class = FilerImageForm
                else:
                    form_class = FilerFileForm
                upload = request.FILES.values()[0]
                filer_form = form_class(
                    {
                        'owner': request.user.pk,
                        'original_filename': upload.name,
                        'is_public': True,
                    },
                    {
                        'file': upload
                    }
                )
                if filer_form.is_valid():
                    obj = filer_form.save()  # commit=False
                    data = {
                        'message': 'ok',
                        'file': self.get_file_detail_dict(obj),
                    }
        return JsonResponse(data=data)

    def get_model_perms(self, *args, **kwargs):
        """
        It seems this is the only way to hide this admin in the app_index :(
        """
        return {
            'add': False,
            'change': False,
            'delete': False,
        }
