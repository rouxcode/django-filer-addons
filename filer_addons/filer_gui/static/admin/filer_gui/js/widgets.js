/* global django */

/*
TODO:
- cleanup edit url code
- add click action on image
*/
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

    var api = {
        'update_widget_elements': update_widget_elements,
    }

    $.fn.filer_gui_file_widget = plugin;

    $doc.on('ready', init);
    $doc.on('formset:added', inline_add);

    // Ugly hack to be sure to have a filer-gui lookup dismiss
    var is_lookup_original = true;
    var dismiss_lookup_original = window.dismissRelatedImageLookupPopup;

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

        init_widget(widget);

        return widget;
    };

    function init_widget(widget) {
        widget._timer;
        widget._file_type = widget.$.data('file-type');
        widget._messages = {
            $all: $('.fg-message', widget.$),
            $upload_error: $('.fg-message.upload_error', widget.$),
            $wrong_file_type: $('.fg-message.wrong-file-type', widget.$)
        };
        widget._text = {
            no_file: widget.$.data('text-no-file')
        };
        widget._urls = {
            file_detail: widget.$.data('file-detail-url'),
            file_upload: widget.$.data('file-upload-url')
        };
        widget.$parent = widget.$.parent().addClass('fg-related-widget-wrapper');
        widget.$rawid = $('.rawid-input', widget.$);
        widget.$add = $('.add-related-filer', widget.$);
        widget.$add[0]._widget = widget;
        widget.$edit = $('.edit-related-filer', widget.$);
        widget.$edit[0]._widget = widget;
        widget.$remove = $('.remove-related-filer', widget.$);
        widget.$remove[0]._widget = widget;
        widget.$lookup = $('.related-lookup-filer', widget.$);
        widget.$lookup[0]._widget = widget;
        widget.$preview = $('.preview', widget.$);
        widget.$dz = $('.uploader', widget.$);
        widget._nofile_template = '<span class="no-file">__txt__</span>';
        widget.hide_all_messages = function() {
            window.clearTimeout(widget._timer);
            widget._messages.$all.removeClass( 'visible' );
        };
        widget.show_message = function( key ) {
            window.clearTimeout(widget._timer);
            widget._timer = window.setTimeout(widget.hide_all_messages, 8000);
            widget._messages[ key ].addClass( 'visible' );
        };
        widget._update_widget = function(data) {
            update_widget(widget, data);
        };

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
    };

    function setup_uploader(widget) {
        widget._dz_template = $('.dz-preview-template', widget.$).html();
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
            widget.hide_all_messages();
            widget.$dz.trigger('click');
        };

        function on_drop(e) {
            widget.hide_all_messages();
        };

        function on_accept(file, done) {
            widget.$dz.addClass('dz-accepted');
            done();
        };

        function on_error(file, msg) {
            widget.hide_all_messages();
            widget.show_message('$wrong_file_type');
            widget._dz.removeFile(file);
        };

        function on_success(file, data) {
            widget.hide_all_messages();
            widget.$dz.removeClass('dz-accepted');
            widget._dz.removeAllFiles();
            update_widget_elements(widget, data.file);
        };
    };

    function no_action( e ) {
        e.preventDefault()
    }

    function edit(e) {
        e.preventDefault();
        if(this._widget.$edit.attr('href')) {
            this._widget.hide_all_messages();
            $(this).trigger(events.edit_start);
            show_edit_popup(this);
        }
    };

    function lookup(e) {
        e.preventDefault();

        // Ugly hack to be sure to have a filer-gui lookup dismiss
        is_lookup_original = false;

        // if no _widget init the widget
        if(!this._widget) {
            // Ugly hack, we need a better way to init an inline add
            $(this).parent().parent().parent().each(plugin_widget)
        }

        this._widget.hide_all_messages();
        $(this).trigger(events.lookup_start);
        showRelatedObjectLookupPopup(this);
    };

    // TODO get html from template
    function remove(e) {
        e.preventDefault();
        this._widget.hide_all_messages();
        this._widget.$rawid.val('');
        this._widget.$preview.html(
            '<span class="no-file">' + this._widget._text.no_file + '</span>'
        );
        update_links(this._widget);

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

        // Ugly hack to be sure to have a filer-gui lookup dismiss
        if( is_lookup_original === true ) {
            dismiss_lookup_original(win, obj_id, thumb_url, file_name);
        } else {
            var id = window.windowname_to_id(win.name);
            var widget = widget_map[id];

            win.close();
            is_lookup_original = false;

            if(widget) {
                widget.$.trigger(events.lookup_end);
                update_widget(widget, obj_id);
            }
        }

    };

    function update_widget(widget, file_id) {
        var file_id = file_id ? file_id : widget.$rawid.val();
        var conf = {
            url: widget._urls.file_detail,
            method: 'POST',
            success: on_success,
            data: {
                filer_file: file_id,
                csrfmiddlewaretoken: csrf,
            }
        }
        var request = $.ajax(conf);

        widget.hide_all_messages();

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

        if(widget._file_type === 'image' && widget._file_type != data.file_type) {
            widget.show_message('$wrong_file_type')
        } else {
            widget.$rawid.val(data.file_id)
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
        }
    };

    function update_links(widget) {
        var edit_url;
        var value = widget.$rawid.val();
        var tmpl = widget.$edit.data('href-template');

        widget.$preview.off().removeClass('clickable');

        if(value) {
            widget.$remove.removeClass('inactive');
            widget.$edit.removeClass('inactive');
            if(widget._edit_url) {
                edit_url = widget._edit_url;
            } else {
                edit_url = tmpl.replace('__fk__', value);
            }
            widget.$edit.attr('href', edit_url);
            widget.$preview.addClass('clickable');
            widget.$preview.on(
                'click',
                function(e) {
                    e.preventDefault();
                    widget.$edit.trigger('click');
                }
            );
        } else {
            widget.$remove.addClass('inactive');
            widget.$edit.removeAttr('href').addClass('inactive');
            widget.$preview.html(
                widget._nofile_template.replace(
                    '__txt__',
                    widget._text.no_file
                )
            );
        }
    };

    function inline_add(event, $row, formset_ame) {
        $('.filer-gui-file-widget', $row).filer_gui_file_widget();
    };

    return api;

})(django.jQuery);
