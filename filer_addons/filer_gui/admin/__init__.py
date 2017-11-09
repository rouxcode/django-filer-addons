from __future__ import unicode_literals

from django.contrib import admin

from .api import FilerGuiAdmin
from .folder import FilerGuiFolderAdmin
from ..models import FilerGuiFile, FilerGuiFolder


admin.site.register(FilerGuiFile, FilerGuiAdmin)
admin.site.register(FilerGuiFolder, FilerGuiFolderAdmin)
