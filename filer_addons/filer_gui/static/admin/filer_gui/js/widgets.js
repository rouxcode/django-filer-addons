/* global django */

var FilerGuiWidgets = (function($){
    'use strict';

    var csrf;
    var $body;
    var $doc = $(document);
    var widget_map = {};
    var events = {
        lookup_changed: $.Event('filer-gui:lookup-changed')
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
        widget.$.on('filer-gui:lookup-changed', on_lookup_changed);
        widget.$add.on('click', add);
        widget.$edit.on('click', edit);
        widget.$lookup.on('click', lookup);

        return widget;
    };

    function on_lookup_changed(e) {
        update_links(this);
    };

    function update_links(widget) {
        var value = widget.$rawid.val();
        var tmpl = widget.$edit.data('href-template');
        if(value) {
            console.log(value)
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
        var event = $.Event('django:change-related');
        $(this).trigger(event);
        show_related_object_popup(this);
    };

    function lookup(e) {
        e.preventDefault();
        var event = $.Event('django:lookup-related');
        $(this).trigger(event);
        showRelatedObjectLookupPopup(this);
    };

    function show_related_object_popup(link) {
        var href = link.href;
        var name = id_to_windowname(link.id.replace(/^lookup_/, ''));
        var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
        win.focus();

        // TODO find a proper way to close the file change popup
        win.onunload = dissmiss_related_window;

        function dissmiss_related_window(e) {
            if(e.target.URL !== 'about:blank') {
                win.close()
            }
        }
    };



    function dissmiss_lookup_window(win, obj_id, thumb_url, file_name) {
        var conf;
        var request;
        var id = window.windowname_to_id(win.name);
        var widget = widget_map[id];

        if(widget) {
            widget.$rawid.val(obj_id);
            conf = {
                url: widget._urls.file_detail,
                method: 'POST',
                success: update_preview,
                data: {
                    filer_file: obj_id,
                    csrfmiddlewaretoken: csrf,
                }
            }
            request = $.ajax(conf);
        }

        win.close();

        function update_preview(data, status, xhr) {
            var html;
            if(data.message === 'ok') {
                if(widget._file_type === 'image') {
                    html = '<img class="thumbnail-img"'
                         + ' src="' + data.file.thumb_url + '"'
                         + ' alt="' + data.file.label + '">'
                         + '<span class="label">'
                         + data.file.label
                         + '</span>';
                } else {
                    html = '<img class="icon-img"'
                         + ' src="' + thumb_url + '"'
                         + ' alt="' + file_name + '">'
                         + '<span class="label">' + file_name + '</span>'
                }
                widget.$preview.html(html);
                widget.$.trigger(events.lookup_changed);
            } else {
                console.error(data.error);
            }
        };
    };


})(django.jQuery);