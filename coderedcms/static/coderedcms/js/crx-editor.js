/*
Wagtail CRX (https://www.coderedcorp.com/cms/)
Copyright 2018-2022 CodeRed LLC
License: https://github.com/coderedcorp/coderedcms/blob/dev/LICENSE
@license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
*/

$(document).ready(function(){
    $(document).on('click', '.crx-collapsible button', function(){
        var $target = $(this).parent().find('.crx-collapsible-target');

        if (!$(this).parent().hasClass('collapsed')) {
            $(this).parent().addClass('collapsed');
            $target.hide('fast');
        } else {
            $(this).parent().removeClass('collapsed');
            $target.show('fast');
        }
    });
});

/* @license-end */
