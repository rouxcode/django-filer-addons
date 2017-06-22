from __future__ import unicode_literals

import logging

from filer.fields.file import (
    AdminFileWidget,
    AdminFileFormField as BaseFileFormField,
    FilerFileField as BaseFileField,
)
from filer.fields.image import (
    FilerImageField as BaseImageField,
)

from .widgets import FilerGuiFileWidget, FilerGuiImageWidget


__all__ = [
    'FilerFileField',
    'FilerImageField',
]


logger = logging.getLogger(__name__)


class AdminFileFormField(BaseFileFormField):
    widget = FilerGuiFileWidget

    def __init__(self, rel, queryset, to_field_name, *args, **kwargs):
        self.widget = self.get_widget(widget=kwargs.pop('widget', None))
        super(AdminFileFormField, self).__init__(
            rel,
            queryset,
            to_field_name,
            *args,
            **kwargs
        )

    def get_widget(self, widget=None):
        # TODO accept instance
        if not widget:
            widget = self.widget
        elif not issubclass(widget, AdminFileWidget):
            msg = '{} must be a subclass of filer.AdminFileWidget'.format(
                self._meta.name
            )
            raise logger.error(msg)
        return widget


class FilerFileField(BaseFileField):
    default_form_class = AdminFileFormField


class AdminImageFormField(AdminFileFormField):
    widget = FilerGuiImageWidget


class FilerImageField(BaseImageField):
    default_form_class = AdminImageFormField
