import os
import tempfile

# from django.conf import settings
from django.core.files import File
from filer.tests import create_image


def create_django_file(filename='test.jpg', size=(800, 800, )):
    """
    returns django file object that can be used in a file field
    :param filename: ie test.jpg
    :param size: tuple, ie (800, 600, )
    :return: django file object
    """
    pil_image = create_image(size=size)
    temp_dir = tempfile.mkdtemp()
    path_filename = os.path.join(temp_dir, filename)
    pil_image.save(path_filename, 'JPEG')
    django_file = File(open(path_filename, 'rb'), name=filename)
    return django_file
