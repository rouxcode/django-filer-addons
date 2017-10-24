from __future__ import unicode_literals

import os
import uuid
import datetime

from filer.utils.files import get_valid_filename
from django.template.defaultfilters import slugify


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
    return os.path.join(str(uuid.uuid4())[:8], filename)


def very_short_uuid4(instance, filename):
    """
    very short (2chars) uuid4 path and the filename
    https://stackoverflow.com/a/13484764/1029469
    at most about 1100 folders will be created, and files distributed within
    """
    filename = get_valid_filename(filename)
    return os.path.join(str(uuid.uuid4())[:2], filename)


def db_folder(instance, filename):
    """
    tries to get the db folder's name, and use this.
    """
    foldername = ''
    if instance.folder:
        foldername = slugify(instance.folder.name)
    filename = get_valid_filename(filename)
    return os.path.join(foldername, filename)


def complete_db_folder(instance, filename):
    """
    get the db folder's name, it's parents, it's parents. etc.
    """

    foldername = ''
    if instance.folder:
        folder = instance.folder
        foldername = slugify(instance.folder.name)
        while folder.parent:
            foldername = os.path.join(slugify(folder.parent.name), foldername)
            folder = folder.parent
    filename = get_valid_filename(filename)
    return os.path.join(foldername, filename)


def year(instance, filename):
    """
    yyyy/filename.jpg
    """
    foldername = datetime.date.today().strftime('%Ys')
    filename = get_valid_filename(filename)
    return os.path.join(foldername, filename)


def year_month(instance, filename):
    """
    yyyy-mm/filename.jpg
    """
    foldername = datetime.date.today().strftime('%Y-%m')
    filename = get_valid_filename(filename)
    return os.path.join(foldername, filename)
