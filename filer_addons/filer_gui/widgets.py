from __future__ import unicode_literals

import logging

import django
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
# from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

# compat thing!
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


logger = logging.getLogger(__name__)
DJANGO_LEGACY = django.VERSION < (1, 9)
THUMBNAIL_SIZE = (300, 100)

# TODO get rid of coded file types
FILE_TYPE_CHOICES = [
    ('file', 'File'),
    ('image', 'Image'),
]


# FIXME remove all file_type related code
class FilerGuiFileWidget(ForeignKeyRawIdWidget):
    """
    Advanced ForeignKeyRawIdWidget with preview and nice select
    new version
    """

    # FIXME find a better way do determin the file_type
    file_type = 'file'  # needet for widget html data and js
    template_name = 'admin/filer_gui/widgets/admin_file.html'

    class Media:
        if DJANGO_LEGACY:
            css = {
                'all': [
                    'admin/filer_gui/css/filer_gui_legacy.css',
                ]
            }
        else:
            css = {
                'all': [
                    'admin/filer_gui/css/filer_gui.css',
                ]
            }
        js = [
            'admin/filer_gui/js/dropzone.js',
            'admin/filer_gui/js/widgets.js',
        ]

    def render(self, name, value, attrs=None, renderer=None):
        # Pre Django 1.11 has no renderer
        if hasattr(self, '_render'):
            return super(FilerGuiFileWidget, self).render(
                name,
                value,
                attrs,
                renderer
            )
        else:
            return self.legacy_render(name, value, attrs)

    def get_context(self, name, value, attrs):
        context = super(FilerGuiFileWidget, self).get_context(
            name,
            value,
            attrs
        )
        file_object = self.file_object_for_value(value)
        rawid_input = self.get_rawid_input(name, value, attrs)

        context.update({
            'file_type': self.file_type,
            'file_object': file_object,
            'rawid_input': rawid_input,
            'lookup_url': '{}{}'.format(
                self.get_lookup_url(file_object),
                self.get_lookup_url_params_as_str()
            ),
            'edit_url_template': '{}{}'.format(
                self.get_edit_url_template(),
                self.get_edit_url_params_as_str()
            ),
        })
        return context

    def get_edit_url_template(self):
        opts = self.rel.model._meta
        url = reverse(
            "admin:{}_{}_{}".format(opts.app_label, self.file_type, 'change'),
            current_app=self.admin_site.name,
            args=['__fk__']
        )
        return url

    def get_edit_url_params_as_str(self):
        params = self.url_parameters()
        params['_popup'] = 1
        if params:
            url = '?' + '&'.join(
                '{}={}'.format(k, v) for k, v in params.items()
            )
        else:
            url = ''
        return url

    def get_lookup_url(self, obj=None):
        # TODO check what file list display we need to show
        if obj:
            url = obj.logical_folder.get_admin_directory_listing_url_path()
        else:
            url = reverse('admin:filer-directory_listing-last')
        return url

    def get_lookup_url_params_as_str(self):
        params = self.url_parameters()
        params['_pick'] = 'file'
        if params:
            url = '?' + '&'.join(
                '{}={}'.format(k, v) for k, v in params.items()
            )
        else:
            url = ''
        return url

    def get_rawid_input(self, name, value, attrs):
        attrs.setdefault('class', 'rawid-input')
        attrs_str = ' '.join('{}="{}"'.format(k, v) for k, v in attrs.items())
        html = '<input type="text" name="{}" value="{}" {}/>'.format(
            name,
            value or '',
            attrs_str
        )
        return mark_safe(html)

    def file_object_for_value(self, value):
        try:
            key = self.rel.get_related_field().name
            obj = self.rel.to._default_manager.get(**{key: value})
        except: # NOQA
            obj = None
        return obj

    def legacy_render(self, name, value, attrs=None):
        file_object = self.file_object_for_value(value)
        if attrs is None:
            attrs = {}
        context = {
            'file_object': file_object,
            'file_type': self.file_type,
            'rawid_input': self.get_rawid_input(name, value, attrs),
            'lookup_url': '{}{}'.format(
                self.get_lookup_url(),
                self.get_lookup_url_params_as_str()
            ),
            'edit_url_template': '{}{}'.format(
                self.get_edit_url_template(),
                self.get_edit_url_params_as_str()
            ),
            'widget': {
                'name': name,
            },
        }
        return mark_safe(render_to_string(self.template_name, context))


class FilerGuiImageWidget(FilerGuiFileWidget):

    # TODO find a better way do determin the file_type
    file_type = 'image'  # needet for widget html data and js
    template_name = 'admin/filer_gui/widgets/admin_image.html'
