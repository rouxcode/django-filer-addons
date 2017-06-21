var FilerGuiWidgets = (function($){
    'use strict';

    var $body;
    var $doc = $(document);

    $.fn.filer_gui_file_widget = plugin;

    $doc.on('ready', init);

    function init() {
        $body = $('body');
        $('.filer-gui-file-widget').filer_gui_file_widget();
    };

    function plugin() {
        return this.each(widget);
    };

    function widget(i) {
        var element = this;
        element.$ = $(this);
        element.$parent = element.$.parent();

        remove_default_related_links();

        function remove_default_related_links() {
            $('> .related-widget-wrapper-link', element.$parent).remove();
        }

        return element;
    }

})(django.jQuery);