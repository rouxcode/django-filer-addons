from __future__ import unicode_literals

from django import template
from django.urls import reverse


register = template.Library()


@register.inclusion_tag(
    'admin/filer_gui/tags/folder_actions.html',
    takes_context=True
)
def filer_gui_folder_actions(context, folder=None):
    if folder:
        add_folder_url = reverse(
            'admin:filer_gui_filerguifolder_add',
            args=[folder.id]
        )
    else:
        add_folder_url = reverse(
            'admin:filer_gui_filerguifolder_add'
        )
    return {
        'add_folder_url': add_folder_url,
    }


@register.inclusion_tag(
    'admin/filer_gui/tags/folder_list.html',
    takes_context=True
)
def filer_gui_folder_list(context, folder_list):
    context.update({
        'folder_list': folder_list,
    })
    return context


@register.inclusion_tag(
    'admin/filer_gui/tags/file_list.html',
    takes_context=True
)
def filer_gui_file_list(context, file_list):
    return {}
