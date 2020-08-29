/*
CodeRed CMS (https://www.coderedcorp.com/cms/)
Copyright 2018-2019 CodeRed LLC
License: https://github.com/coderedcorp/coderedcms/blob/dev/LICENSE
@license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
*/

$(document).ready(function(){
    $(document).on('click', '.codered-collapsible button', function(){
        var $fieldset = $(this).parent().find('fieldset');

        if (!$(this).parent().hasClass('collapsed')) {
            $(this).parent().addClass('collapsed');
            $fieldset.hide('fast');
        } else {
            $(this).parent().removeClass('collapsed');
            $fieldset.show('fast');
        }
    });
});

/* @license-end */
