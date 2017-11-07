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
            no_file: widget.$.data('text-no-file')
        }
        widget._urls = {
            file_detail: widget.$.data('file-detail-url'),
            file_upload: widget.$.data('file-upload-url')
        }
        widget.$parent = widget.$.parent();
        widget.$rawid = $('.rawid-input', widget.$);
        widget.$add = $('.add-related-filer', widget.$);
        widget.$edit = $('.edit-related-filer', widget.$);
        widget.$remove = $('.remove-related-filer', widget.$);
        widget.$remove[0]._widget = widget;
        widget.$lookup = $('.related-lookup-filer', widget.$);
        widget.$preview = $('.preview', widget.$);
        widget.$dz = $('.uploader', widget.$);

        widget_map[widget.$rawid.attr('id')] = widget;

        // remove django default related links
        $('> .related-widget-wrapper-link', widget.$parent).remove();

        // setup links initialy
        update_links(widget);

        // catch events
        widget.$edit.on('click', edit);
        widget.$lookup.on('click', lookup);
        widget.$remove.on('click', remove);

        // setup dropzonejs uploader
        if(widget.$dz.length > 0) {
            setup_uploader(widget);
        } else {
            widget.$add.remove();
        }

        return widget;
    };

    function setup_uploader(widget) {
        widget._dz_template = $('.dz-preview-template', widget.$).remove().html();
        widget._dz_conf = {
            url: widget._urls.file_upload,
            paramName: 'file',
            uploadMultiple: false,
            params: {
                file_type: widget._file_type,
                csrfmiddlewaretoken: csrf
            },
            maxFiles: 1,
            previewTemplate: widget._dz_template,
            accept: on_accept,
            drop: on_drop,
            error: on_error,
            success: on_success
        };

        if(widget._file_type === 'image') {
            widget._dz_conf.acceptedFiles = 'image/*';
        }

        widget._dz = new Dropzone(widget.$dz[0], widget._dz_conf);
        widget.$add.on('click', add);

        function add(e) {
            e.preventDefault();
            widget.$dz.trigger('click');
        };

        function on_drop(e) {
            widget.$dz.removeClass('file-type-error');
        }

        function on_accept(file, done) {
            widget.$dz.addClass('dz-accepted');
            done();
        };

        function on_error(file, msg) {
            widget.$dz.addClass('file-type-error');
            widget._dz.removeFile(file);
        };

        function on_success(file, data) {
            widget.$dz.removeClass('dz-accepted');
            widget._dz.removeAllFiles();
            widget.$rawid.val(data.file.file_id);
            update_widget_elements(widget, data.file);
        };
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

    // TODO get html from template
    function remove(e) {
        e.preventDefault();
        this._widget.$rawid.val('');
        this._widget.$preview.html(
            '<span class="no-file">' + this._widget._text.no_file + '</span>'
        );
    };

    function show_edit_popup(link) {
        var href = link.href;
        var name = id_to_windowname(link.id.replace(/^edit_/, ''));
        var win = window.open(
            href,
            name,
            'height=500,width=800,resizable=yes,scrollbars=yes'
        );
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
            if(data.message === 'ok') {
                update_widget_elements(widget, data.file)
            } else {
                console.error(data.error);
            }
        }
    };

    function update_widget_elements(widget, data) {
        var css;
        var html;
        var url;
        var edit_url = undefined;
        if(widget._file_type === 'image') {
            css = 'thumbnail-img'
            url = data.thumb_url;
        } else {
            css = 'icon-img'
            url = data.icon_url;
        }
        if(data.edit_url) {
            widget._edit_url = data.edit_url + '?_to_field=id&_popup=1';
        } else {
            widget._edit_url = undefined;
        }
        widget.$preview.html(
            '<img class="' + css + '" src="' + url + '" alt="' + data.label + '">'
          + '<span class="label">' + data.label + '</span>'
        );
        update_links(widget);
    };

    function update_links(widget) {
        var value = widget.$rawid.val();
        var tmpl = widget.$edit.data('href-template');
        if(value) {
            widget.$remove.removeClass('inactive');
            widget.$edit.removeClass('inactive');
            if(widget._edit_url) {
                widget.$edit.attr('href', widget._edit_url);
            } else {
                widget.$edit.attr('href', tmpl.replace('__fk__', value));
            }
        } else {
            widget.$remove.addClass('inactive');
            widget.$edit.removeAttr('href').addClass('inactive');
            widget.$preview.html('<span class="no-file">' + widget._text.no_file + '</span>');
        }
    };

})(django.jQuery);
