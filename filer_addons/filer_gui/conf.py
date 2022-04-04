from django.conf import settings


CHANGE_LIST_THUMB_SIZE = getattr(
    settings, 'FILER_ADDONS_CHANGE_LIST_THUMB_SIZE',
    (140, 100,),
)

FIELD_THUMB_SIZE = getattr(
    settings, 'FILER_ADDONS_FIELD_THUMB_SIZE',
    (110, 80,),
)
