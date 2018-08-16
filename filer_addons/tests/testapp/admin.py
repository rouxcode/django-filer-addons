from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from .models import (
    FilerTest,
    FilerUglyFileInlineModel,
    FilerUglyImageInlineModel,
    FilerNewImageInlineModel, FilerNewFileInlineModel)
from filer_addons.filer_gui.admin.multiupload import (
    FilerMultiUploadInlineMixin,
)


class MultiUploadStackedInline(
    FilerMultiUploadInlineMixin,
    admin.StackedInline
):
    model = FilerUglyFileInlineModel
    file_field = 'filer_file_ugly'
    fields = ['name', 'filer_file_ugly', ]


class MultiUploadTabularInline(
    FilerMultiUploadInlineMixin,
    admin.TabularInline
):
    model = FilerUglyImageInlineModel
    file_field = 'filer_image_ugly'
    fields = ['name', 'filer_image_ugly', ]


class NewMultiUploadStackedInline(
    FilerMultiUploadInlineMixin,
    admin.StackedInline
):
    model = FilerNewFileInlineModel
    file_field = 'filer_file'
    fields = ['name', 'filer_file', ]


class NewMultiUploadTabularInline(
    FilerMultiUploadInlineMixin,
    admin.TabularInline
):
    model = FilerNewImageInlineModel
    file_field = 'filer_image'
    fields = ['name', 'filer_image', ]


class FilerTestAdminForm(forms.ModelForm):

    class Meta:
        model = FilerTest
        fields = '__all__'


@admin.register(FilerTest)
class FilerTestAdmin(admin.ModelAdmin):
    form = FilerTestAdminForm
    list_filter = [
        'name',
    ]
    inlines = [
        MultiUploadStackedInline,
        MultiUploadTabularInline,
        NewMultiUploadStackedInline,
        NewMultiUploadTabularInline,
    ]
    readonly_fields = [
        # 'parent',
    ]
    raw_id_fields = [
        'filer_file_raw',
    ]

    fieldsets = [
        ('Settings', {
            'classes': ['section'],
            'fields': [

            ],
        }),
        ('Filer default widgets', {
            'classes': ['section'],
            'fields': [
                'filer_file_ugly',
                'filer_image_ugly',
            ],
        }),
        ('Widget Test', {
            'classes': ['section'],
            'fields': [
                'name',
                'filer_file_raw',
                'filer_file',
                'filer_image',
            ]
        })
    ]
