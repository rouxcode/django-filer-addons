from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FilerGuiConfig(AppConfig):
    name = 'filer_addons.filer_gui'
    verbose_name = _('File management')
