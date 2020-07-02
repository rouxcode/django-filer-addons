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
        self.resolve_for_class(Image)
        self.resolve_for_class(File)

    def resolve_for_class(self, cls):
        # exit("untested code! exiting!")
        # file dups
        temp = cls.objects.values('sha1').annotate(Count('id')).values('sha1').order_by().filter(id__count__gt=1)
        # keep the oldes, that is probably longest in search indexes...
        duplicates = cls.objects.filter(sha1__in=temp).order_by('uploaded_at')
        print("resolving duplicates in {}!".format(cls.__name__))
        # relation business
        model_links = [
            rel.get_accessor_name()
            for rel in model_get_all_related_objects(cls)
        ]
        print(model_links)
        # state
        done = {}
        count = 0
        for file in duplicates:
            # do we have an original!?
            if file.sha1 in done:
                objs = []
                for link in model_links:
                    relation = getattr(file, link, None)
                    if getattr(relation, 'all', None):
                        for usage_obj in relation.all():
                            # print(relation.field.name)
                            # print(usage_obj)
                            # print(usage_obj.__class__)
                            # print(usage_obj.id)
                            setattr(usage_obj, relation.field.name, cls.objects.get(id=done[file.sha1]))
                            usage_obj.save()
                # DELETE
                print("delete {}".format(file.path))
                file.delete()
                count += 1
            else:
                # first time, keep this file
                done[file.sha1] = file.id
        print("resolved {} duplicates in {}!".format(count, cls.__name__))


def model_get_all_related_objects(model):
    """
    https://docs.djangoproject.com/en/2.0/ref/models/meta/
    """
    if getattr(model._meta, 'get_all_related_objects', None):
        return model._meta.get_all_related_objects()
    else:
        return [
            f for f in model._meta.get_fields()
            if (f.one_to_many or f.one_to_one) and
            f.auto_created and not f.concrete
        ]


