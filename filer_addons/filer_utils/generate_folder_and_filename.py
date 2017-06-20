import os
import uuid

from filer.utils.files import get_valid_filename


def no_subfolders(instance, filename):
    """
    for the minimalist
    attention, in case of filename collisions, files might get renamed to
    "originalname_huievad676asd.ext", which is automatically done by the
    django storage backend
    """
    return get_valid_filename(filename)


def short_uuid4(instance, filename):
    """
    short (8chars) uuid4 path and the filename
    https://stackoverflow.com/a/13484764/1029469
    should be safe enough for most cases
    """
    filename = get_valid_filename(filename)
    return os.path.join(uuid.uuid4()[:8], filename)
