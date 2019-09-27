var InlineUpload = (function($){
    'use strict';

    var csrf;
    var $inlines;

    var inline_selector = '.uploadinline-wrap'
    var $doc = $(document);

    $(init);
    $.fn.upload_inline = init_plugins;

    function init() {
        csrf = get_csrf();
        $inlines = $(inline_selector).upload_inline()
    };

    function init_plugins(){
        return this.each(inline_uploader);
    };

    function inline_uploader(){
        var inline = this;
        inline.$ = $( this );
        inline.$title = $('h2:first', inline.$);
        // inline.$add_inline = $('.add-row a', inline.$);
        // not available from the beginning!
        inline.add_inline_selector = '.add-row a'
        inline._conf = inline.$.data('uploadinline');

        setup_uploader(inline);

        return inline;
    };

    function setup_uploader(inline) {
        inline.$dz = get_dropzone_element(inline);
        inline._dz_preview = $('.dz-preview-template', inline.$dz).html()
        inline._dz_conf = {
            url: inline._conf.upload_url,
            paramName: 'file',
            uploadMultiple: false,
            params: {
                file_type: inline._conf.file_type,
                csrfmiddlewaretoken: csrf
            },
            maxFiles: 100,
            previewTemplate: inline._dz_preview,
            accept: on_accept,
            drop: on_drop,
            error: on_error,
            success: on_success
        };

        if(inline._conf.file_type === 'image') {
            inline._dz_conf.acceptedFiles = 'image/*';
        }

        inline._dz = new Dropzone(inline.$dz[0], inline._dz_conf);

        function add(e) {
            e.preventDefault();
        };

        function on_drop(e) {
            inline._dz.removeAllFiles();
        };

        function on_accept(file, done) {
            inline.$dz.addClass('dz-accepted');
            done();
        };

        function on_error(file, msg) {
            var $preview = $(file.previewElement);
            var $msg = $('.dz-preview-message', $preview)
            $msg.html(msg);
            $msg.removeClass('hidden');
            $preview.addClass('dz-error');
        };

        function on_success(file, data) {
            if(data.message === 'ok') {
                $doc.on('formset:added', row_added);
                $(inline.add_inline_selector, inline.$).trigger('click');
                // inline.$add_inline.trigger('click');
                $doc.off('formset:added');
                inline._dz.removeFile(file);
            } else {
                on_error(file, 'upload error');
            }

            function row_added(event, $row, name) {
                var $widget = $('.filer-gui-file-widget', $row)
                var widget = $widget[0];
                if(!widget.$) {
                    $widget.filer_gui_file_widget();
                }
                widget._update_widget(data.file.file_id);
            };
        };
    };

    function get_dropzone_element(inline) {
        var css_class = 'filer-gui-upload-inline-dropzone';
        var $html = $(
            '<div class="' + css_class + '">'
          + '<div class="dz-message dz-info needsclick">'
          + 'Drop files here or click to upload files from your computer'
          + '</div>'
          + get_dz_preview()
          + '</div>'
        ).insertAfter(inline.$title);
        return $('.' + css_class, inline.$);
    };

    function get_dz_preview(){
        var html = '<div class="dz-preview-template">'
                 + '<div class="dz-preview dz-file-preview">'
                 + '<div class="dz-file-preview">'
                 + '<div class="dz-progress">'
                 + '<span class="dz-upload" data-dz-uploadprogress></span>'
                 + '</div>'
                 + '<div class="dz-thumbnail"></div>'
                 + '<div class="dz-preview-message hidden"></div>'
                 + '<div data-dz-name class="dz-name"></div>'
                 + '</div>'
                 + '</div>'
                 + '</div>';
        return html;
    };

    function get_csrf() {
        var $f = $('[name="csrfmiddlewaretoken"]:first');
        if($f.length < 1 ) {
            console.error('file_gui upload inline: no csrf found');
        } else {
            return $f.val();
        }
    };

})(django.jQuery);
