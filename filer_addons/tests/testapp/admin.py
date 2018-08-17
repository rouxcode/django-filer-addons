from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from .models import (
    FilerNewImageInlineModel, FilerNewFileInlineModel, FilerNewFieldTest, FilerOriginalFieldTest,
    FilerOriginalFileInlineModel, FilerOriginalImageInlineModel)
from filer_addons.filer_gui.admin.upload_inline import (
    UploadInlineMixin,
)


class MultiUploadStackedInline(
    UploadInlineMixin,
    admin.StackedInline
):
    model = FilerOriginalFileInlineModel
    file_field = 'filer_file_original'
    fields = ['name', 'filer_file_original', ]


class MultiUploadTabularInline(
    UploadInlineMixin,
    admin.TabularInline
):
    model = FilerOriginalImageInlineModel
    file_field = 'filer_image_original'
    fields = ['name', 'filer_image_original', ]


class NewMultiUploadStackedInline(
    UploadInlineMixin,
    admin.StackedInline
):
    model = FilerNewFileInlineModel
    file_field = 'filer_file'
    fields = ['name', 'filer_file', ]


class NewMultiUploadTabularInline(
    UploadInlineMixin,
    admin.TabularInline
):
    model = FilerNewImageInlineModel
    file_field = 'filer_image'
    fields = ['name', 'filer_image', ]


@admin.register(FilerOriginalFieldTest)
class FilerTestAdmin(admin.ModelAdmin):
    inlines = [
        MultiUploadStackedInline,
        MultiUploadTabularInline,
    ]

@admin.register(FilerNewFieldTest)
class FilerTestAdmin(admin.ModelAdmin):
    inlines = [
        NewMultiUploadStackedInline,
        NewMultiUploadTabularInline,
    ]

    # readonly_fields = [
    #     # 'parent',
    # ]
    # raw_id_fields = [
    #     'filer_file_raw',
    # ]
    #
    # fieldsets = [
    #     ('Settings', {
    #         'classes': ['section'],
    #         'fields': [
    #
    #         ],
    #     }),
    #     ('Filer default widgets', {
    #         'classes': ['section'],
    #         'fields': [
    #             'filer_file_original',
    #             'filer_image_original',
    #         ],
    #     }),
    #     ('Widget Test', {
    #         'classes': ['section'],
    #         'fields': [
    #             'name',
    #             'filer_file_raw',
    #             'filer_file',
    #             'filer_image',
    #         ]
    #     })
    # ]
