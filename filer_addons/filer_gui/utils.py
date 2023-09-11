from __future__ import unicode_literals

import os


IMAGE_EXT = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.svg',
]


def file_is_image_by_name(file_name):
    ext = os.path.splitext(file_name)[1].lower()
    return ext in IMAGE_EXT
