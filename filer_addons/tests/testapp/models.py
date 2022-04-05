from django.db import models
from filer.fields.file import FilerFileField as OriginalFilerFileField
from filer.fields.image import FilerImageField as OriginalFilerImageField
from filer.models import File
from filer_addons.filer_gui.fields import FilerFileField, FilerImageField


class FilerOriginalFieldTest(models.Model):
    name = models.CharField(
        max_length=150,
    )
    filer_file_raw = models.ForeignKey(
        File,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    filer_file_original = OriginalFilerFileField(
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        related_name='file_original_filertest',
    )
    filer_image_original = OriginalFilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
        related_name='image_original_filertest',
    )

    def __str__(self):
        return '{}'.format(self.name)


class FilerNewFieldTest(models.Model):
    name = models.CharField(
        max_length=150,
    )
    filer_file_raw = models.ForeignKey(
        File,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    filer_file = FilerFileField(
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        related_name='file_filertest',
    )
    filer_image = FilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
        related_name='image_filertest',
    )

    def __str__(self):
        return '{}'.format(self.name)


class FilerOriginalImageInlineModel(models.Model):
    filer_test = models.ForeignKey(
        FilerOriginalFieldTest,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=150,
        default='',
        blank=True,
    )
    filer_image_original = OriginalFilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{}'.format(self.name)


class FilerOriginalFileInlineModel(models.Model):
    filer_test = models.ForeignKey(
        FilerOriginalFieldTest,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=150,
        default='',
        blank=True,
    )
    filer_file_original = OriginalFilerFileField(
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{}'.format(self.name)


class FilerNewImageInlineModel(models.Model):
    filer_test = models.ForeignKey(
        FilerNewFieldTest,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=150,
        default='',
        blank=True,
    )
    filer_image = FilerImageField(
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{}'.format(self.name)


class FilerNewFileInlineModel(models.Model):
    filer_test = models.ForeignKey(
        FilerNewFieldTest,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=150,
        default='',
        blank=True,
    )
    filer_file = FilerFileField(
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{}'.format(self.name)
