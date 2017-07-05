from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from .models import FilerTest, FilerTestInlineModel
from filer_addons.filer_gui.inlines import FilerMultiUploadInlineMixin


class MultiUploadStackedInline(
    FilerMultiUploadInlineMixin,
    admin.StackedInline
):
    model = FilerTestInlineModel
    file_field = 'filer_image'


class MultiUploadTabularInline(
    FilerMultiUploadInlineMixin,
    admin.TabularInline
):
    model = FilerTestInlineModel
    file_field = 'filer_image'


class FilerTestAdminForm(forms.ModelForm):

    class Meta:
        model = FilerTest
        fields = '__all__'


@admin.register(FilerTest)
class FilerTestAdmin(admin.ModelAdmin):
    form = FilerTestAdminForm
    # inlines = [MultiUploadStackedInline, MultiUploadTabularInline, ]
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
                'parent',
                'name',
            ],
        }),
        ('Filer default widgets', {
            'classes': ['section'],
            'fields': [
                'filer_file_raw',
                'filer_file',
                'filer_image',
            ],
        }),
        ('Widget Test', {
            'classes': ['section'],
            'fields': [
                'filer_file_raw',
                'filer_file',
                'filer_image',
            ],
        }),
    ]


"""
('Widget Reference', {
    'classes': ['section'],
    'fields': [
        'filer_file_ugly',
        'filer_image_ugly',
    ],
}),
"""
