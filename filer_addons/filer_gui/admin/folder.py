from __future__ import unicode_literals

from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from ..models import File, FilerGuiFolder


csrf_protect_m = method_decorator(csrf_protect)


class FilerGuiFolderAdminForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = FilerGuiFolder
        widgets = {
            'parent': forms.HiddenInput,
            'owner': forms.HiddenInput,
        }


class FilerGuiFolderAdmin(admin.ModelAdmin):

    file_model = File
    form = FilerGuiFolderAdminForm
    list_filter = [
        'name'
    ]

    def add_view(self, request, folder_id=None, form_url='',
                 extra_context=None):
        return self.changeform_view(
            request,
            None,
            folder_id,
            form_url,
            extra_context
        )

    @csrf_protect_m
    def changelist_view(self, request, folder_id=None, viewtype=None):
        folder = self.get_folder(request, folder_id)
        context = {
            'folder': folder,
            'folder_list': self.get_folder_list(request, folder),
            'file_list': self.get_file_list(request, folder),
        }
        return super(FilerGuiFolderAdmin, self).changelist_view(
            request,
            extra_context=context
        )

    @csrf_protect_m
    @transaction.atomic
    def changeform_view(self, request, object_id=None, folder_id=None,
                        form_url='', extra_context=None):
        self._folder = self.get_folder(request, folder_id)
        return super(FilerGuiFolderAdmin, self).changeform_view(
            request,
            object_id=None,
            form_url='',
            extra_context=None
        )

    def get_changeform_initial_data(self, request):
        initial = super(FilerGuiFolderAdmin, self).get_changeform_initial_data(
            request
        )
        initial.update({
            'parent': self._folder,
            'owner': request.user,
        })
        return initial

    def get_folder(self, request, folder_id=None):
        if not folder_id:
            return None
        try:
            return self.get_queryset(request).get(pk=folder_id)
        except self.model.DoesNotExist:
            return None

    def get_folder_list(self, request, folder):
        if folder:
            kwargs = {'parent_id': folder.id}
        else:
            kwargs = {'parent_id__isnull': True}
        return self.get_queryset(request).filter(**kwargs)

    def get_file_list(self, request, folder):
        return []

    def get_queryset(self, request):
        qs = super(FilerGuiFolderAdmin, self).get_queryset(request)
        return qs

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = [
            url(
                r'^$',
                self.admin_site.admin_view(self.changelist_view),
                {'viewtype': 'root'},
                name='{}_{}_list_root'.format(*info)
            ),
            url(
                r'^last/$',
                self.admin_site.admin_view(self.changelist_view),
                {'viewtype': 'last'},
                name='{}_{}_list_last'.format(*info)
            ),
            url(
                r'^(?P<folder_id>\d+)/list/$',
                self.admin_site.admin_view(self.changelist_view),
                {'viewtype': 'sub'},
                name='{}_{}_list'.format(*info)
            ),
            url(
                r'^add/$',
                self.admin_site.admin_view(self.add_view),
                name='{}_{}_add'.format(*info)
            ),
            url(
                r'^(?P<folder_id>\d+)/add/$',
                self.admin_site.admin_view(self.add_view),
                name='{}_{}_add'.format(*info)
            ),
        ]
        return urls + super(FilerGuiFolderAdmin, self).get_urls()
