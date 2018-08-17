from django.conf import settings
from django.forms import widgets
from django import forms
from filer.models import File


"""
we need:
- element in form or on page with a custom classname and data attrs,
  totrigger js
possible solutions:
- 1 hack change form, add stuff there. only one uploader per plugin possible!
- 2 use custom form with custom widget. widget can be positioned in form...
- 3 check def get_fields() (no luck for now)
    https://stackoverflow.com/questions/8007095/dynamic-fields-in-django-admin

implemented:
- mix between 1 and 2 (as a form is definitly needed)
"""


class UploadPluginForm(forms.ModelForm):
    filer_gui_added_files = forms.ModelMultipleChoiceField(
        queryset=File.objects.all(),
        required=False
    )


class UploadPluginMixin(object):
    """
    config for users of this mixin
    upload_child_plugin: plugin type to create, for example 'ImagePlugin'
    upload_file_field: filer file field on the created plugin
    add_first: add at first position? defaults to False
    """
    upload_child_plugin = None
    upload_file_field = 'file'
    add_first = False
    # end config
    form = UploadPluginForm
    # upload_folder = get_folder_by_path('uploads', True)
    change_form_template = (
        'admin/filer_gui/inlines/multiupload_plugin_changeform.html'
    )

    @property
    def media(self):
        original_media = super(UploadPluginMixin, self).media
        js = (
            # settings.STATIC_URL + 'filer/js/libs/dropzone.min.js',
            # settings.STATIC_URL + 'filer/js/addons/dropzone.init.js',
            settings.STATIC_URL + 'admin/filer_gui/js/multiupload_plugin.js',
        )
        css = {
            'all': [
                settings.STATIC_URL
                + 'admin/filer_gui/css/multiupload_base.css',
            ]
        }
        new_media = widgets.Media(js=js, css=css)
        return original_media + new_media

    def save_model(self, request, obj, form, change):
        response = super(UploadPluginMixin, self).save_model(
            request, obj, form, change
        )
        # print "-----"
        # print form.cleaned_data['filer_gui_added_files']
        for file in form.cleaned_data['filer_gui_added_files']:
            placeholder = obj.placeholder
            parent_plugin = obj
            plugin_data = {
                self.upload_file_field: file,
            }
            # cms is not a dependency, so we import locally.
            from cms.api import add_plugin
            tree_position = 'last-child'
            if self.add_first:
                tree_position = 'first-child'
            added_plugin = add_plugin(
                 placeholder,
                 self.upload_child_plugin,
                 obj.language,
                 tree_position,
                 parent_plugin,
                 **plugin_data
            )
            if self.add_first:
                added_plugin.position = 0
                added_plugin.save()
        return response
