# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-05 05:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file
import filer_addons.filer_gui.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_filertestinlinemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filertest',
            name='filer_file',
            field=filer_addons.filer_gui.fields.FilerFileField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_filertest', to='filer.File'),
        ),
        migrations.AlterField(
            model_name='filertest',
            name='filer_file_ugly',
            field=filer.fields.file.FilerFileField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_ugly_filertest', to='filer.File'),
        ),
        migrations.AlterField(
            model_name='filertestinlinemodel',
            name='filer_file',
            field=filer_addons.filer_gui.fields.FilerFileField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_filerinlinetest', to='filer.File'),
        ),
        migrations.AlterField(
            model_name='filertestinlinemodel',
            name='filer_file_ugly',
            field=filer.fields.file.FilerFileField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_ugly_filerinlinetest', to='filer.File'),
        ),
        migrations.AlterField(
            model_name='filertestinlinemodel',
            name='name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
