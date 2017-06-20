from __future__ import unicode_literals

import logging

from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.http import urlencode
from django.utils.safestring import mark_safe


logger = logging.getLogger(__name__)


# TODO get rid of filer code and implement rawid field
class FilerGuiFileWidget(ForeignKeyRawIdWidget):
    """
    Adwanced ForeignKeyRawIdWidget with preview and nice select
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
    template_name = 'admin/filer_gui/widgets/admin_image.html'
