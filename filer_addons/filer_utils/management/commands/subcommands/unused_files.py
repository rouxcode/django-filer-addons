from django.utils.encoding import force_text
from filer.models import File, Folder, Image

from .base import SubcommandsCommand


class UnusedFilesCommand(SubcommandsCommand):
    help_string = 'Delete files that have are not used in any filer field.' \
                  'WARNING: Specifying' \
                  '\'+\' as related name disables reverse lookup,' \
                  'and will not catch up here!'
    command_name = 'unused_files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete them!'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Show them all'
        )
        parser.add_argument(
            '--folder-id',
            action='store',
            dest='folder_id',
            default=False,
            help='Only within folder with id X'
        )

    def handle(self, *args, **options):
        # deprecated!
        # related = File._meta.get_all_related_objects()
        # replaced by: https://docs.djangoproject.com/en/1.11/ref/models/meta/
        self.unused_for_file_type(File, **options)
        self.unused_for_file_type(Image, **options)

    def unused_for_file_type(self, model_cls, **options):
        filter_kwargs = {}
        for f in model_cls._meta.get_fields():
            if (
                f.one_to_many or f.one_to_one
            ) and f.auto_created and not f.concrete:
                if f.related_name:
                    filter_kwargs[f.related_name] = None
                else:
                    filter_kwargs[f.name] = None
        if options['folder_id']:
            try:
                folder_id = int(options['folder_id'])
            except ValueError:
                raise ValueError('folder-id must be an integer')
            try:
                folder = Folder.objects.get(pk=folder_id)
            except Folder.DoesNotExist:
                raise ValueError(
                    'Folder with id {} not found!'.format(folder_id))
            descendants = folder.get_descendants(include_self=True)
            filter_kwargs['folder__in'] = descendants
        unused = model_cls.objects.filter(**filter_kwargs)
        amount = unused.count()
        for file in unused:
            if options['verbose']:
                self.stdout.write(force_text(file))
            if options['delete']:
                file.delete()
        self.stdout.write(
            "%s unused %s found." % (str(amount), model_cls.__name__))
