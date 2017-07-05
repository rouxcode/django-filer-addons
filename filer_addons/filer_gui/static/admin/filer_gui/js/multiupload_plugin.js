var FilerMultiUploadPlugin = ( function ( $ ) {
    'use strict';

    var $plugins;

    // public api
    var api = {
        reset_all: reset_all,
        reset_by_selector: reset_by_selector
    };

    $.fn.filer_multiupload_plugin = filer_multiupload_plugin;

    $(document).ready( init );

    function init() {
        $('#content .filer-gui-multiupload-plugin').filer_multiupload_plugin();
    };

    function filer_multiupload_plugin(custom_options) {
        $plugins = this;
        var i;
        for (i=0; i<$plugins.length; i++) {
            init_plugin($plugins[i], custom_options);
        }
        return this;
    };

    function init_plugin(plugin, custom_options) {

        plugin.$ = $(plugin);
        var default_options = {

        }
        var options = $.extend(default_options, custom_options);

        var $uploaded_files_field_wrap = $('#content .field-filer_gui_added_files').hide(0);
        var $uploaded_files_field = $uploaded_files_field_wrap.find('select');

        // init dropzone
        var $dropzone = plugin.$;
        $("#content form fieldset:last").append($dropzone);
        var dropzone = new Dropzone($dropzone[0], {
            'url': plugin.$.attr('data-upload-url'),
            'createImageThumbnails': false,
            'clickable': [plugin.$.find('.filer-gui-select-file')[0]],
            'init': function() {
                // this.on("uploadprogress", file_upload_complete });
                this.on("success", file_upload_complete );
            }
        });

        function file_upload_complete(file, response) {
            var $option = $uploaded_files_field.find('option[value="' + response.file_id + '"]');
            if ($option.size() < 1) {
                $option = $('<option value="' + response.file_id + '">' + response.label + '</option>')
                $uploaded_files_field.append($option);
            }
            $option.prop('selected', true);
        };

        return this;

    };

    // global methods!

    function reset_all() {

    };

    function reset_by_selector( selector ) {
        var plugin = $plugins.filter( selector );
        // plugin._active;
    };

    return api;

})( django.jQuery );
