/* global django */

var FilerGuiWidgets = (function($){
    'use strict';

    var csrf;
    var $body;
    var $doc = $(document);
    var widget_map = {};
    var events = {
        edit_end: $.Event('filer-gui:edit-end'),
        edit_start: $.Event('filer-gui:edit-start'),
        lookup_end: $.Event('filer-gui:lookup-end'),
        lookup_start: $.Event('filer-gui:lookup-start')
    };

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
        widget._text = {
            'no_file': widget.$.data('text-no-file')
        }
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

        // setup links initialy
        update_links(widget);

        // catch events
        widget.$add.on('click', add);
        widget.$edit.on('click', edit);
        widget.$lookup.on('click', lookup);

        return widget;
    };

    function update_links(widget) {
        var value = widget.$rawid.val();
        var tmpl = widget.$edit.data('href-template');
        if(value) {
            widget.$edit.attr('href', tmpl.replace('__fk__', value)).removeClass('inactive');
        } else {
            widget.$edit.removeAttr('href').addClass('inactive');
            widget.$preview.html('<span class="no-file">' + widget._text.no_file + '</span>');
        }
    };

    function add(e) {
        e.preventDefault();
        console.log('hop derzue')
    };

    function edit(e) {
        e.preventDefault();
        $(this).trigger(events.edit_start);
        show_edit_popup(this);
    };

    function lookup(e) {
        e.preventDefault();
        $(this).trigger(events.lookup_start);
        showRelatedObjectLookupPopup(this);
    };

    function show_edit_popup(link) {
        var href = link.href;
        var name = id_to_windowname(link.id.replace(/^edit_/, ''));
        var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
        win.focus();

        // TODO find a proper way to close the file change popup
        win.onunload = dissmiss_related_window;

        function dissmiss_related_window(e) {
            if(e.target.URL !== 'about:blank') {
                win.close();
                var id = window.windowname_to_id(win.name);
                var widget = widget_map[id];
                if(widget) {
                    widget.$.trigger(events.edit_end);
                    update_widget(widget);
                }
            }
        }
    };

    function dissmiss_lookup_window(win, obj_id, thumb_url, file_name) {
        var id = window.windowname_to_id(win.name);
        var widget = widget_map[id];

        win.close();

        if(widget) {
            widget.$.trigger(events.lookup_end);
            widget.$rawid.val(obj_id);
            update_widget(widget);
        }
    };

    function update_widget(widget) {
        var conf = {
            url: widget._urls.file_detail,
            method: 'POST',
            success: on_success,
            data: {
                filer_file: widget.$rawid.val(),
                csrfmiddlewaretoken: csrf,
            }
        }
        var request = $.ajax(conf);

        function on_success(data, status, xhr) {
            var html;
            var url;
            if(data.message === 'ok') {
                if(widget._file_type === 'image') {
                    css = 'thumbnail-img'
                    url = data.file.thumb_url;
                } else {
                    css = 'icon-img'
                    url = data.file.icon_url;
                }
                widget.$preview.html(
                    '<img class="' + css + '" src="' + url + '" alt="' + data.file.label + '">'
                  + '<span class="label">' + data.file.label + '</span>'
                );
                update_links(widget);

            } else {
                console.error(data.error);
            }
        }
    };


})(django.jQuery);