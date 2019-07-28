(
    function ($) {
        var $content_md = $('#div_id_content_md');
        var $content_ck = $('#div_id_content_ck');
        var $use_md = $('input[name=use_md]');
        var $switch_editor = function (use_md) {
            if (use_md) {
                $content_md.show();
                $content_ck.hide();
            } else {
                $content_md.hide();
                $content_ck.show();
            }
        }
        $use_md.on('click',function () {
            $switch_editor($(this).is(':checked'));
        });
        $switch_editor($use_md.is(':checked'));
    }
)(jQuery);