from __future__ import unicode_literals

import logging

import django
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.http import urlencode
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

    def file_object_for_value(self, value):
        try:
            key = self.rel.get_related_field().name
            obj = self.rel.to._default_manager.get(**{key: value})
        except:
            obj = None
        return obj

    def get_rawid_input(self, name, value, attrs):
        attrs.setdefault('class', 'vForeignKeyRawIdAdminField')
        attrs_str = ' '.join('{}="{}"'.format(k, v) for k, v in attrs.items())
        html = '<input type="text" name="{}" value="{}" {}/>'.format(
            name,
            value or '',
            attrs_str
        )
        return mark_safe(html)

    def legacy_render(self, name, value, attrs=None):
        rel_to = self.rel.to
        if attrs is None:
            attrs = {}
        if rel_to in self.admin_site._registry:
            # The related object is registered with the same AdminSite
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
            'file_object': self.file_object_for_value(value),
            'rawid_input': self.get_rawid_input(name, value, attrs),
            'related_url': '{}{}'.format(related_url, url),
            'widget': {
                'name': name,
            },
        }
        return mark_safe(render_to_string(self.template_name, context))


# TODO get rid of filer code and implement rawid field
class FilerGuiFileWidgetOld(ForeignKeyRawIdWidget):
    """
    Adwanced ForeignKeyRawIdWidget with preview and nice select
    old version based und django-filer
    """

    template_name = 'admin/filer_gui/widgets/admin_file.html'

    class Media:
        css = {
            'all': [
                'admin/filer_gui/css/filer_gui.css',
            ]
        }
        """
        js = (
            'filer/js/libs/dropzone.min.js',
            'filer/js/addons/dropzone.init.js',
            'filer/js/addons/popup_handling.js',
            'filer/js/addons/widget.js',
        )
        """

    def get_url_params(self):
        params = self.url_parameters()
        params['_pick'] = 'file'
        params['_popup'] = '1'
        if params:
            url_params = '?' + urlencode(sorted(params.items()))
        else:
            url_params = ''
        return url_params

    def get_rawid_input(self, name, value, attrs):
        attrs.setdefault('class', 'vForeignKeyRawIdAdminField')
        attrs_str = ' '.join('{}="{}"'.format(k, v) for k, v in attrs.items())
        html = '<input type="text" name="{}" value="{}" {}/>'.format(
            name,
            value or '',
            attrs_str
        )
        return mark_safe(html)

    def get_context(self, name, value, attrs):
        obj, lookup_url = self.object_and_lookup_url_for_value(value)
        css_id = attrs.get('id', 'id_image_x')
        url_params = self.get_url_params()
        context = {
            'rawid_input': self.get_rawid_input(name, value, attrs),
            'lookup_url': '%s%s' % (lookup_url, url_params),
            'edit_url': '%s%s' % (lookup_url, url_params),
            'object': obj,
            'name': name,
            'css_id': css_id,
        }
        return context

    """
    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, renderer)


    def _render(self, template_name, context, renderer=None):
        # check if django provides us a renderer (django>=1.11)
        # if not use render_to_string
        try:
            from django.forms.renderers import get_default_renderer
        except ImportError:
            return mark_safe(render_to_string(template_name, context))
        if renderer is None:
            renderer = get_default_renderer()
        return mark_safe(renderer.render(template_name, context))
    """

    def object_and_lookup_url_for_value(self, value):
        try:
            key = self.rel.get_related_field().name
            obj = self.rel.to._default_manager.get(**{key: value})
        except:
            obj = None
        if obj:
            url = obj.logical_folder.get_admin_directory_listing_url_path()
        else:
            url = reverse('admin:filer-directory_listing-last')
        return obj, url


class FilerGuiImageWidget(FilerGuiFileWidget):
    pass
    # template_name = 'admin/filer_gui/widgets/admin_image.html'
