from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from .models import (
    FilerTest,
    FilerUglyTest,
    FilerUglyFileInlineModel,
    FilerUglyImageInlineModel,
)
from filer_addons.filer_gui.admin.multiupload import (
    FilerMultiUploadInlineMixin,
)


@admin.register(FilerUglyTest)
class FilerUglyTestAdmin(admin.ModelAdmin):
    pass


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


class FilerTestAdminForm(forms.ModelForm):

    class Meta:
        model = FilerTest
        fields = '__all__'


@admin.register(FilerTest)
class FilerTestAdmin(admin.ModelAdmin):
    form = FilerTestAdminForm
    inlines = [
        # MultiUploadStackedInline,
        # MultiUploadTabularInline,
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
                'name',
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
                'filer_file_raw',
                'filer_file',
                'filer_image',
            ]
        })
    ]

    """
    ('Widget Test', {
        'classes': ['section'],
        'fields': [
            'filer_file_raw',
            'filer_file',
            'filer_image',
            'filer_image_ugly_2',
        ],
    }),
    """
