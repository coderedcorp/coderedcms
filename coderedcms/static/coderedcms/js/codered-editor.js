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
