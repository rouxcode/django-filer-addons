from __future__ import unicode_literals
import os

from django.db.models.signals import post_save
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
    if instance.id and instance.file:
        if old_name is None:
            old_instance = File.objects.get(pk=instance.id)
            old_name = old_instance.file.name
        old_name = os.path.basename(old_name)
        new_name = get_valid_filename(instance.original_filename)
        if not old_name == new_name:
            # rename!
            # print "do rename: %s to %s" % (old_name, new_name)
            existing_file = open(instance.file.path, mode='rb')
            new_file = DjangoFile(existing_file)
            instance.file.delete(False)  # remove including thumbs
            instance.file.save(new_name, new_file, save=False)
            # print instance.file.name
            # todo: prevent deadlock, when storagem gives the _x5sx4sd suffix!
            # do it here, original_filename is not updated correctly else!
            instance.save()
            existing_file.close()


@receiver(
    post_save,
    sender='filer.File',
    dispatch_uid="filer_addons_unfiled_file_to_folder",
)
@receiver(
    post_save,
    sender='filer.Image',
    dispatch_uid="filer_addons_unfiled_image_to_folder",
)
def filer_unfiled_to_folder(sender, instance, **kwargs):
    """
    check if a file is unfiled, if yes, put into default folder.
    ATTENTION: this signal must be registered before the duplicate detection signal => for when only
    duplicates in the same folder need to be detected! (put in folder first, then detect duplicate)
    """
    if not conf.FILER_ADDONS_UNFILED_HANDLING.get('move_unfiled', None):
        return
    created_only = conf.FILER_ADDONS_UNFILED_HANDLING.get('created_only', False)
    if created_only and not kwargs.get('created', None):
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


@receiver(
    post_save,
    sender='filer.File',
    dispatch_uid="filer_addons_prevent_duplicates_file",
)
@receiver(
    post_save,
    sender='filer.Image',
    dispatch_uid="filer_addons_prevent_duplicates_image",
)
def filer_duplicates_and_rename(sender, instance, **kwargs):
    """
    check for duplicates, dont allow them!
    as this is post save, it will ELIMINATE ALL DUPLICATES of a file,
    if there are...this can be quite dangerous, but also be wonderfull ;-)
    """
    if not conf.FILER_ADDONS_DUPLICATE_HANDLING.get('prevent'):
        return
    created_only = conf.FILER_ADDONS_DUPLICATE_HANDLING.get('created_only', False)
    if created_only and not kwargs.get('created', None):
        return
    file_obj = instance
    duplicates = File.objects.exclude(pk=file_obj.id).filter(sha1=file_obj.sha1)
    # narrow down? depends.
    if conf.FILER_ADDONS_DUPLICATE_HANDLING.get('same_folder_required', None):
        duplicates = duplicates.filter(folder=file_obj.folder)
    if conf.FILER_ADDONS_DUPLICATE_HANDLING.get('same_filename_required', None):
        # TODO: is this slugified somehow??!
        duplicates = duplicates.filter(
            original_filename=file_obj.original_filename
        )
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
        # to be defined: set some more fields from duplicate, if filled?!
        # arf dont touch django magic
        # instance._uncommitted_filefields = []
        # instance._state = duplicate._state
        instance.save()
        check_rename(instance, old_name=old_name)
    else:
        """
        when updating a file in a files detail view, it already has the new,
        correct name leaving this here, for example when manipulating files
        (and original_filename) programmatically.
        """
        check_rename(instance)

