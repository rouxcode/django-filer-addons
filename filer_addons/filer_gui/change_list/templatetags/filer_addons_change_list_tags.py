from django import template
from easy_thumbnails.files import get_thumbnailer
from filer.models import Image

from .. import conf


register = template.Library()


@register.simple_tag(takes_context=False)
def filer_addons_change_list_thumb(obj, ):
    if isinstance(obj, Image):
        thumbnailer = get_thumbnailer(obj.file)
        thumbnail_options = {'size': conf.CHANGE_LIST_THUMB_SIZE}
        try:
            return thumbnailer.get_thumbnail(thumbnail_options).url
        except (InvalidImageFormatError, FileNotFoundError) as e:
            pass
    return '/static/filer/icons/file-unknown.svg'
