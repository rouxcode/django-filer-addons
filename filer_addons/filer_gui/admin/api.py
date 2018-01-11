from __future__ import unicode_literals

from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse

from filer import settings as filer_settings

from ..models import File, Image
from ..utils import file_is_image_by_name

# FIXME get it from settings
from ..widgets import FILE_TYPE_CHOICES, THUMBNAIL_SIZE


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


class FilerGuiAdmin(admin.ModelAdmin):

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
            edit_url = reverse('admin:filer_image_change', args=[obj.id])
        else:
            thumb_url = obj.icons['48']
            edit_url = reverse('admin:filer_file_change', args=[obj.id])
        data = {
            'label': obj.label,
            'file_id': obj.id,
            'file_url': obj.url,
            'icon_url': obj.icons['48'],
            'thumb_url': thumb_url,
            'edit_url': edit_url,
            'file_type': obj.file_type.lower(),
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
                # TODO: .values()[0] was for python2, is this correct?
                # upload = request.FILES.values()[0]
                upload = request.FILES.get('file')
                # TODO: get rid of this distinction and find a proper way
                # to get the correct model form
                form_class = None
                if file_is_image_by_name(upload.name):
                    form_class = FilerImageForm
                else:
                    form_class = FilerFileForm
                filer_form = form_class(
                    {
                        'owner': request.user.pk,
                        'original_filename': upload.name,
                        'is_public': filer_settings.FILER_IS_PUBLIC_DEFAULT,
                    },
                    {
                        'file': upload
                    }
                )
                if filer_form.is_valid():
                    # TODO check why settings.FILER_IS_PUBLIC_DEFAULT
                    # needs to be set to True for the following to work
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
