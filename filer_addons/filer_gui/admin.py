from __future__ import unicode_literals

from django.contrib import admin

from .models import FilerGuiFile


@admin.register(FilerGuiFile)
class FilerGuiAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = []
        return urls

    def get_model_perms(self, *args, **kwargs):
        """
        It seems this is the only way to hide this admin in the app_index :(
        """
        return {
            'add': False,
            'change': False,
            'delete': False,
        }
