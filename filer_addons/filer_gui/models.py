from filer.models import File, Image


__all__ = [
    File,
    Image,
    'FilerGuiFile',
]


class FilerGuiFile(File):

    class Meta(File.Meta):
        proxy = True
