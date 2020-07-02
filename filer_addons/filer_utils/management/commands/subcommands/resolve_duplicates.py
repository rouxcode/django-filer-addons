# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from filer.models import File
from filer.models import Image

from .base import SubcommandsCommand


class ResolveDuplicatesCommand(SubcommandsCommand):
    help_string = _('resolve duplicates (remove detected duplicates, assign original instead)')
    command_name = 'resolve_duplicates'

    def handle(self, *args, **options):
        self.resolve_for_class(File)
        self.resolve_for_class(Image)

    def resolve_for_class(self, cls):
        # exit("untested code! exiting!")
        # file dups
        temp = cls.objects.values('sha1').annotate(Count('id')).values('sha1').order_by().filter(id__count__gt=1)
        # keep the oldes, that is probably longest in search indexes...
        duplicates = cls.objects.filter(sha1__in=temp).order_by('uploaded_at')
        duplicates_count = duplicates.distinct().count()
        print("resolving {} duplicates in {}!".format(duplicates_count, cls.__name__))
        done = {}
        for file in duplicates:
            # do we have an original!?
            if file.sha1 in done:
                # we have an original. go through all related objects for this file.
                try:
                    file._meta._related_objects_cache
                except AttributeError:
                    file._meta._fill_related_objects_cache()
                for related in file._meta._related_objects_cache:
                    # get all of the same model that use this file
                    kwargs = {
                        related.field.name: file.id,
                    }
                    affected = related.model.objects.filter(**kwargs)
                    # update them to use the original
                    kwargs = {
                        related.field.name: done[file.sha1],
                    }
                    affected.update(**kwargs)
                # DELETE
                file.delete()
            else:
                # first time, keep this file
                done[file.sha1] = file.id
