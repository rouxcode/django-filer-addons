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
        # relation business
        model_links = [
            rel.get_accessor_name()
            for rel in model_get_all_related_objects(file.__class__)
        ]
        # state
        done = {}
        for file in duplicates:
            # do we have an original!?
            if file.sha1 in done:
                objs = []
                for link in model_links:
                    relation = getattr(file, link, None)
                    print(relation)
                    if getattr(relation, 'all', None):
                        for usage_obj in relation.all():
                            print(usage_obj)
                            # kwargs = {
                            #     related.field.name: file.id,
                            # }
                            # affected = related.model.objects.filter(**kwargs)
                            # # update them to use the original
                            # kwargs = {
                            #     related.field.name: done[file.sha1],
                            # }
                            # affected.update(**kwargs)
                    # DELETE
                    file.delete()
            else:
                # first time, keep this file
                done[file.sha1] = file.id




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


