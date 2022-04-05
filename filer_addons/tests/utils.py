import os
import tempfile

# from django.conf import settings
from django.core.files import File
from filer.utils.compatibility import PILImage, PILImageDraw


def create_image(mode='RGB', size=(800, 600)):
    image = PILImage.new(mode, size)
    draw = PILImageDraw.Draw(image)
    x_bit, y_bit = size[0] // 10, size[1] // 10
    draw.rectangle((x_bit, y_bit * 2, x_bit * 7, y_bit * 3), 'red')
    draw.rectangle((x_bit * 2, y_bit, x_bit * 3, y_bit * 8), 'red')
    return image


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


def create_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    superuser = User.objects.create_superuser('admin',
                                              'admin@free.fr',
                                              'secret')
    return superuser
