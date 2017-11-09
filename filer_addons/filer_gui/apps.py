from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FilerGuiConfig(AppConfig):
    name = 'filer_addons.filer_gui'
    verbose_name = _('File management')
