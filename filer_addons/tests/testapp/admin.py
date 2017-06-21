from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from .models import FilerTest


class FilerTestAdminForm(forms.ModelForm):

    class Meta:
        model = FilerTest
        fields = '__all__'


class FilerTestInline(admin.StackedInline):
    model = FilerTest
    form = FilerTestAdminForm


@admin.register(FilerTest)
class FilerTestAdmin(admin.ModelAdmin):
    form = FilerTestAdminForm
    # inlines = [FilerTestInline]
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
