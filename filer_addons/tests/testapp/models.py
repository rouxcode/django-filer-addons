from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from filer.fields.file import FilerFileField as UglyFilerFileField
from filer.fields.image import FilerImageField as UglyFilerImageField
from filer.models import File
from filer_addons.filer_gui.fields import FilerFileField, FilerImageField


@python_2_unicode_compatible
class FilerTest(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=150,
    )
    filer_file_raw = models.ForeignKey(
        File,
        null=True,
        blank=False,
    )
    filer_file = FilerFileField(
        null=True,
        blank=False,
        default=None,
        on_delete=models.SET_NULL,
        related_name='file_filertest',
    )
    filer_image = FilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='image_filertest',
    )
    filer_file_ugly = UglyFilerFileField(
        null=True,
        blank=False,
        default=None,
        on_delete=models.SET_NULL,
        related_name='file_ugly_filertest',
    )
    filer_image_ugly = UglyFilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='image_ugly_filertest',
    )

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class FilerTestInlineModel(models.Model):
    filer_test = models.ForeignKey(
        FilerTest
    )
    name = models.CharField(
        max_length=150,
    )
    filer_image = FilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='image_filertest',
    )

    def __str__(self):
        return '{}'.format(self.name)
