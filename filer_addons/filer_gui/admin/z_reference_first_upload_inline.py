from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.forms import widgets

from filer_addons.filer_gui.fields import FilerImageField, FilerFileField
from filer.fields.image import FilerImageField as OriginalFilerImageField


class FilerMultiUploadInlineMixin(object):

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
        original_media = super(FilerMultiUploadInlineMixin, self).media
        js = (
            settings.STATIC_URL + 'filer/js/libs/dropzone.min.js',
            settings.STATIC_URL + 'admin/filer_gui/js/multiupload_inline.js',
        )
        css = {
            'all': (
                settings.STATIC_URL
                + 'admin/filer_gui/css/multiupload_base.css',
            )
        }
        new_media = widgets.Media(js=js, css=css)
        return original_media + new_media

    @property
    def template(self):
        if isinstance(self, admin.StackedInline):
            return 'admin/filer_gui/inlines/multiupload_stacked.html'
        if isinstance(self, admin.TabularInline):
            return 'admin/filer_gui/inlines/multiupload_tabular.html'
        raise ImproperlyConfigured(
            'Class {0}.{1} must also derive from'
            ' admin.TabularInline or'
            ' admin.StackedInline'
            .format(self.__module__, self.__class__)
        )

    @property
    def is_filer_gui_field(self):
        field = getattr(self.model, self.file_field, None)
        if field:
            if isinstance(field.field, (FilerImageField, FilerFileField, ),):
                return True
        else:
            raise ImproperlyConfigured(
                'file_field must be set on inline, pointing to the target'
                'file field'
            )

    @property
    def is_image_field(self):
        field = getattr(self.model, self.file_field, None)
        if field:
            if isinstance(field.field, (FilerImageField, OriginalFilerImageField, ),): # NOQA
                return True
        else:
            raise ImproperlyConfigured(
                'file_field must be set on inline, pointing to the target'
                'file field'
            )
