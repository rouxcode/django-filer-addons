from django import template
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer
# support very big images
# https://stackoverflow.com/questions/51152059/pillow-in-python-wont-let-me-open-image-exceeds-limit
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = 933120000
from filer.models import Image

from .. import conf


register = template.Library()


@register.simple_tag(takes_context=False)
def filer_gui_file_thumb(obj, context='change_list'):
    if isinstance(obj, Image):
        thumbnailer = get_thumbnailer(obj.file)
        thumbnail_options = {'size': conf.CHANGE_LIST_THUMB_SIZE}
        try:
            return thumbnailer.get_thumbnail(thumbnail_options).url
        except (InvalidImageFormatError, FileNotFoundError) as e:
            pass
    if obj.file and obj.file.path.endswith('.pdf'):
        return '/static/filer/icons/file-pdf.svg'
    return '/static/filer/icons/file-unknown.svg'
