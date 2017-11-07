from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from filer.fields.file import FilerFileField as UglyFilerFileField
from filer.fields.image import FilerImageField as UglyFilerImageField
from filer.models import File
from filer_addons.filer_gui.fields import FilerFileField, FilerImageField


@python_2_unicode_compatible
class FilerTest(models.Model):
    name = models.CharField(
        max_length=150,
    )
    filer_file_raw = models.ForeignKey(
        File,
        null=True,
        blank=True,
    )
    filer_file = FilerFileField(
        null=True,
        blank=True,
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
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='file_ugly_filertest',
    )
    filer_file_ugly_2 = UglyFilerFileField(
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='file_ugly_2_filertest',
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
class FilerUglyTest(models.Model):
    name = models.CharField(
        max_length=150,
    )
    filer_file_ugly = UglyFilerFileField(
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='file_ugly_fileruglytest',
    )
    filer_image_ugly = UglyFilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='image_ugly_fileruglytest',
    )

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class FilerUglyImageInlineModel(models.Model):
    filer_test = models.ForeignKey(
        FilerTest
    )
    name = models.CharField(
        max_length=150,
        default='',
        blank=True,
    )
    filer_image_ugly = UglyFilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class FilerUglyFileInlineModel(models.Model):
    filer_test = models.ForeignKey(
        FilerTest
    )
    name = models.CharField(
        max_length=150,
        default='',
        blank=True,
    )
    filer_file_ugly = UglyFilerFileField(
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '{}'.format(self.name)
