from __future__ import unicode_literals

import json

import django
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.forms import widgets
from django.utils.encoding import force_text
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import (
    FilerFileField as OriginalFilerFileField,
    FilerImageField as OriginalFilerImageField,
)

from filer_addons.filer_gui.fields import FilerImageField, FilerFileField

# compat thing!
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


class UploadInlineMixin(object):
    # TODO: select one or multiple existing files with the file picker!
    # TODO: add at first or last position?
    # TODO: check file_field correctness!

    """
    adds a dropzone at the beginning of the inline. uploaded files will be
    added to the inline, the new file_id being set on the "file_field".
    """
    file_field = 'file'
    # upload_folder = get_folder_by_path('uploads', True)
    extra = 0
    hide_add_inline = False
    # extra_css_class = 'sortable-inline sortable-tabular-inline'

    @property
    def media(self):
        original_media = super(UploadInlineMixin, self).media
        js = (
            settings.STATIC_URL + 'admin/filer_gui/js/dropzone.js',
            settings.STATIC_URL + 'admin/filer_gui/js/inline.upload.js',
        )
        css = {
            'all': (
                settings.STATIC_URL
                + 'admin/filer_gui/css/filer_gui.css',
            )
        }
        new_media = widgets.Media(js=js, css=css)
        return original_media + new_media

    @property
    def template(self):
        if isinstance(self, admin.StackedInline):
            return 'admin/filer_gui/inlines/upload_stacked.html'
        if isinstance(self, admin.TabularInline):
            return 'admin/filer_gui/inlines/upload_tabular.html'
        raise ImproperlyConfigured(
            'Class {0}.{1} must also derive from'
            ' admin.TabularInline or'
            ' admin.StackedInline'
            .format(self.__module__, self.__class__)
        )

    @property
    def html_data_fields(self):
        data_fields = getattr(
            super(UploadInlineMixin, self),
            'html_data_fields',
            ''
        )
        fields = {
            'upload_url': reverse('admin:file_upload'),
            'file_field': self.get_file_field(),
            'file_type': self.get_file_type(),
            'messages': {
                'generic_upload_error': force_text(_('Upload error')),
            },
        }
        data_fields = '{} data-uploadinline=\'{}\''.format(
            data_fields,
            json.dumps(fields),
        )
        return mark_safe(data_fields)

    @property
    def css_classes(self):
        css_class = 'uploadinline-wrap'
        css_classes = getattr(
            super(UploadInlineMixin, self),
            'css_classes',
            ''
        )
        return '{} {}'.format(css_classes, css_class)

    def get_file_field(self):
        field = getattr(self.model, self.file_field, None)
        field_types = (
            FilerFileField,
            OriginalFilerFileField,
            FilerImageField,
            OriginalFilerImageField,
        )
        if isinstance(field.field, field_types):
            return self.file_field
        else:
            raise ImproperlyConfigured(
                'file_field must be set on inline, pointing to the target'
                'file field'
            )

    def get_file_type(self):
        field = getattr(self.model, self.file_field, None)
        image_types = (
            FilerImageField,
            OriginalFilerImageField,
        )
        file_types = (
            FilerFileField,
            OriginalFilerFileField,
        )
        if isinstance(field.field, image_types):
            return 'image'
        elif isinstance(field.field, file_types):
            return 'file'
        else:
            raise ImproperlyConfigured(
                'file_field must be set on inline, pointing to the target'
                'file field'
            )
