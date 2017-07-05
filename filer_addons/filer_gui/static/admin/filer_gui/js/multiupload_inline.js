var FilerMultiUploadInline = (function ($) {
    'use strict';

    var $plugins;

    // public api
    var api = {
        reset_all: reset_all,
        reset_by_selector: reset_by_selector
    };

    $.fn.filer_multiupload_inline = filer_multiupload_inline;

    $(document).ready(init);

    function init() {
        $('.filer-gui-multiupload-inline').filer_multiupload_inline();
    };

    function filer_multiupload_inline(custom_options) {
        $plugins = this;
        var i;
        for (i = 0; i < $plugins.length; i++) {
            init_plugin($plugins[i], custom_options);
        }
        return this;
    };

    function init_plugin(plugin, custom_options) {

        plugin.$ = $(plugin);

        var default_options = {
            'file_field': plugin.$.attr('data-file-field')
        }
        var options = $.extend(default_options, custom_options);

        // init dropzone
        // TODO: div goes into html? with {% trans %}
        var $dropzone = plugin.$.find('.filer-gui-multiupload-dropzone');
        plugin.$.find(".inline-group h2").after($dropzone);
        var dropzone_conf = {
            url: plugin.$.attr('data-upload-url'),
            'createImageThumbnails': false,
            'clickable': [plugin.$.find('.select-file')[0]],
            init: function () {
                // this.on("uploadprogress", file_upload_complete });
                this.on("success", file_upload_complete);
            }
        }
        var dropzone = new Dropzone($dropzone[0], dropzone_conf);
        // $dropzone.dropzone(dropzone_conf);

        function file_upload_complete(file, response) {
            $(file.previewElement).delay(2000).fadeOut(1000);
            plugin.$.find('.add-row a:first').trigger('click');
            var $row = plugin.$.find('div.inline-related:visible:last:not(.tabular), tr.form-row:visible:last');
            var $field_wrap = $row.find('.field-' + options.file_field);
            $field_wrap.find('.vForeignKeyRawIdAdminField').val(response.file_id);
            $field_wrap.find('.js-file-selector .description_text').html(response.label);
            $field_wrap.find('.thumbnail_img')
                .removeClass('hidden')
                .attr('src', response.thumbnail)
                .parent().attr('href', response.link);
            ;
            $field_wrap.find('.js-file-selector .related-lookup').addClass('related-lookup-change');
            $field_wrap.find('.js-file-selector .filerClearer').removeClass('hidden');
            $field_wrap.find('.dz-message').addClass('hidden');
        };
        return this;
    };

    // global methods!

    function reset_all() {

    };

    function reset_by_selector(selector) {
        var plugin = $plugins.filter(selector);
        // plugin._active;
    };

    return api;

})(django.jQuery);
