from __future__ import unicode_literals

from django.contrib import admin

from .filer_gui import FilerGuiAdmin
from ..models import FilerGuiFile


admin.site.register(FilerGuiFile, FilerGuiAdmin)
