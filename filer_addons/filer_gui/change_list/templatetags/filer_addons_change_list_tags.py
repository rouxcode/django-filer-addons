from django import template
from easy_thumbnails.files import get_thumbnailer
from filer.models import Image

register = template.Library()


@register.simple_tag(takes_context=False)
def filer_addons_change_list_thumb(obj, ):
    if isinstance(obj, Image):
        thumbnailer = get_thumbnailer(obj.file)
        thumbnail_options = {'size': (170, 120)}
        return thumbnailer.get_thumbnail(thumbnail_options).url
    else:
        return obj.icons['48']
