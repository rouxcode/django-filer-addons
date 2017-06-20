from __future__ import unicode_literals

import logging

from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from filer import settings as filer_settings
from filer.fields.file import AdminFileWidget
from filer.models import File


logger = logging.getLogger(__name__)


class FilerGuiFileWidget(AdminFileWidget):

    template_name = 'admin/filer_gui/widgets/admin_file.html'

    class Media:
        css = {
            'all': [
                'admin/filer_addons/css/filer_gui.css',
            ]
        }

        """
        css = {
            'all': [
                'filer/css/admin_filer.css',
                'admin/filer_addons/css/filer_gui.css',
            ]
        }
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
        if 'class' not in attrs:
            # JavaScript looks for this hook.
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        # get only the input html field of ForeignKeyRawIdWidget
        return super(ForeignKeyRawIdWidget, self).render(name, value, attrs)

    def get_context(self, name, value, attrs):
        obj = self.obj_for_value(value)
        css_id = attrs.get('id', 'id_image_x')
        if obj:
            url = obj.logical_folder.get_admin_directory_listing_url_path()
        else:
            url = reverse('admin:filer-directory_listing-last')
        url_params = self.get_url_params()
        context = {
            'rawid_input': self.get_rawid_input(name, value, attrs),
            'lookup_url': '%s%s' % (url, url_params),
            'object': obj,
            'name': name,
            'css_id': css_id,
        }
        return context

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        html = render_to_string(self.template_name, context)
        return mark_safe(html)


class FilerGuiImageWidget(FilerGuiFileWidget):
    template_name = 'admin/filer_gui/widgets/admin_image.html'
