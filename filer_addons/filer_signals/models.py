from __future__ import unicode_literals
import os

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.files.base import File as DjangoFile
from filer.models import File, Folder
from filer.utils.files import get_valid_filename


from . import conf


def check_rename(instance, old_name=None):
    """
    do the rename
    :param instance: filer file instance
    :return:
    """
    # print "check rename"
    if instance.id and instance.file:
        if old_name is None:
            old_instance = File.objects.get(pk=instance.id)
            old_name = old_instance.file.name
        old_name = os.path.basename(old_name)
        new_name = get_valid_filename(instance.original_filename)
        if not old_name == new_name:
            # rename!
            # print "do rename: %s to %s" % (old_name, new_name)
            new_file = DjangoFile(open(instance.file.path, mode='rb'))
            instance.file.delete(False)  # remove including thumbs
            instance.file.save(new_name, new_file, save=False)
            # do it here, original_filename doesnt seem to be updated correctly else!
            instance.save()


@receiver(post_save, sender='filer.File')
def filer_duplicates_and_rename(sender, instance, **kwargs):
    """
    check for duplicates, dont allow them!
    as this is post save, it will ELIMINATE ALL DUPLICATES of a file, if there are!
    this can be quite dangerous, but also be wonderfull ;-)
    """
    # print "check duplicates"
    file_obj = instance
    duplicates = File.objects.filter(sha1=file_obj.sha1, folder=file_obj.folder)
    duplicates = duplicates.exclude(pk=file_obj.id)
    if len(duplicates):
        # print "duplicates found (post save):"
        # print duplicates
        duplicate = None
        for file in duplicates:
            if file.file:
                duplicate = file
        if duplicate is None:
            # duplicate without file is not what we can use!
            return
        instance.delete()
        duplicate = duplicates[0]
        old_name = duplicate.file.name
        instance.id = duplicate.id
        instance.file = duplicate.file
        instance.name = duplicate.name
        instance.name = duplicate.name
        instance.description = duplicate.description
        if hasattr(duplicate, 'subject_location'):
            instance.subject_location = duplicate.subject_location
        # set some more fields from duplicate, if they are filled?!
        # arf dont touch django magic
        # instance._uncommitted_filefields = []
        # instance._state = duplicate._state
        instance.save()
        check_rename(instance, old_name=old_name)
    else:
        # when updating a file in a files detail view, it already has the new, correct name
        # leaving this here, for example when manipulating files (and original_filename) programmatically.
        check_rename(instance)


@receiver(post_save, sender='filer.File')
def filer_unfiled_to_folder(sender, instance, **kwargs):
    """
    check if a file is unfiled, if yes, put into default folder.
    """
    if not conf.FILER_ADDONS_UNFILED_HANDLING.get('move_unfiled', None):
        return
    if not instance.folder:
        default_folder_name = conf.FILER_ADDONS_UNFILED_HANDLING.get(
            'default_folder_name',
            'Unfiled',
        )
        default_folder_list = Folder.objects.filter(name=default_folder_name)
        if default_folder_list.count() > 0:
            default_folder = default_folder_list[0]
        else:
            default_folder = Folder(name=default_folder_name)
            default_folder.save()
        instance.folder = default_folder
        instance.save()


