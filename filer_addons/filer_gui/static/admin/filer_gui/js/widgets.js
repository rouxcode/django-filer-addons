/* global django */

var FilerGuiWidgets = (function($){
    'use strict';

    var csrf;
    var $body;
    var $doc = $(document);
    var widget_map = {};

    $.fn.filer_gui_file_widget = plugin;

    $doc.on('ready', init);
    window.dismissRelatedImageLookupPopup = dissmiss_lookup_window;

    function init() {
        $body = $('body');
        csrf = $('input[name="csrfmiddlewaretoken"]').val();
        $('.filer-gui-file-widget').filer_gui_file_widget();
    };

    function plugin() {
        return this.each(plugin_widget);
    };

    function plugin_widget(i) {
        var widget = this;
        widget.$ = $(this);
        widget._file_type = widget.$.data('file-type');
        widget._urls = {
            file_detail: widget.$.data('file-detail-url')
        }
        widget.$parent = widget.$.parent();
        widget.$rawid = $('.rawid-input', widget.$);
        widget.$add = $('.add-related-filer', widget.$);
        widget.$edit = $('.edit-related-filer', widget.$);
        widget.$lookup = $('.related-lookup-filer', widget.$);
        widget.$preview = $('.preview', widget.$);
        widget_map[widget.$rawid.attr('id')] = widget;

        // remove django default related links
        $('> .related-widget-wrapper-link', widget.$parent).remove();

        widget.$add.on('click', add);
        widget.$edit.on('click', edit);
        widget.$lookup.on('click', lookup);

        return widget;
    };

    function add(e) {
        e.preventDefault();
        console.log('hop derzue')
    };

    function edit(e) {
        e.preventDefault();
        console.log('edschit')
    };

    function lookup(e) {
        e.preventDefault();
        var event = $.Event('django:lookup-related');
        $(this).trigger(event);
        showRelatedObjectLookupPopup(this)
    };

    function dissmiss_lookup_window(win, obj_id, thumb_url, file_name) {
        var conf;
        var request;
        var id = window.windowname_to_id(win.name);
        var widget = widget_map[id];

        win.close();

        if(widget) {
            widget.$rawid.val(obj_id);
            if(widget._file_type === 'file') {
                widget.$preview.html(
                    '<img class="icon-img" src="' + thumb_url + '" alt="' + file_name + '">'
                  + '<span class="label">' + file_name + '</span>'
                )
            } else if(widget._file_type === 'image') {
                conf = {
                    url: widget._urls.file_detail,
                    method: 'POST',
                    success: on_success,
                    data: {
                        filer_file: obj_id,
                        csrfmiddlewaretoken: csrf,
                    }
                }
                request = $.ajax(conf);
            }
        }

        function on_success(data, status, xhr) {
            if(data.message === 'ok') {
                widget.$preview.html(
                    '<img class="thumbnail-img" src="'
                    + data.file.thumb_url
                    + '" alt="' + data.file.label
                    + '">'
                    + '<span class="label">'
                    + data.file.label
                    + '</span>'
                )
            } else {
                console.error(data.error);
            }
        };
    };


})(django.jQuery);