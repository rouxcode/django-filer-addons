from __future__ import unicode_literals

from filer.models import File, Image  # NOQA


class FilerGuiFile(File):

    class Meta(File.Meta):
        proxy = True
