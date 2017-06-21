from __future__ import unicode_literals

import logging

import django
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


logger = logging.getLogger(__name__)
django_legacy = django.VERSION < (1, 9)


class FilerGuiFileWidget(ForeignKeyRawIdWidget):
    """
    Advanced ForeignKeyRawIdWidget with preview and nice select
    new version
    """

    template_name = 'admin/filer_gui/widgets/admin_file.html'

    class Media:
        if django_legacy:
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
            'file_object': file_object,
            'rawid_input': rawid_input,
        })
        return context

    def get_lookup_url(self, obj=None):
        # TODO check what file list display we need to show
        if obj:
            url = obj.logical_folder.get_admin_directory_listing_url_path()
        else:
            url = reverse('admin:filer-directory_listing-last')
        return url

    def get_rawid_input(self, name, value, attrs):
        attrs.setdefault('class', 'vForeignKeyRawIdAdminField')
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
        except:
            obj = None
        return obj

    def legacy_render(self, name, value, attrs=None):
        rel_to = self.rel.to
        file_object = self.file_object_for_value(value)
        if attrs is None:
            attrs = {}
        if rel_to in self.admin_site._registry:
            related_url = reverse(
                'admin:{}_{}_changelist'.format(
                    rel_to._meta.app_label,
                    rel_to._meta.model_name,
                ),
                current_app=self.admin_site.name,
            )

            params = self.url_parameters()
            if params:
                url = '?' + '&amp;'.join(
                    '{}={}'.format(k, v) for k, v in params.items()
                )
            else:
                url = ''
        context = {
            'file_object': file_object,
            'rawid_input': self.get_rawid_input(name, value, attrs),
            'related_url': '{}{}'.format(related_url, url),
            'lookup_url': '{}{}'.format(self.get_lookup_url(file_object), url),
            'widget': {
                'name': name,
            },
        }
        return mark_safe(render_to_string(self.template_name, context))


class FilerGuiImageWidget(FilerGuiFileWidget):
    template_name = 'admin/filer_gui/widgets/admin_image.html'
