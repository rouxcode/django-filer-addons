from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from filer.models import File, Folder, Image  # NOQA


class FilerGuiFile(File):

    class Meta(File.Meta):
        proxy = True


class FilerGuiFolder(Folder):

    class Meta(Folder.Meta):
        proxy = True
        verbose_name = _('Files')
        verbose_name_plural = _('Files')
