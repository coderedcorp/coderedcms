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

    $(document).on('click', 'a.codered-clearcache', function(event) {
        event.preventDefault();
        $el = $(this);
        // show spinner
        $el.addClass('icon icon-spinner');
        oldtext = $el.html();
        $el.html($el.data("clicked-text"));
        // make ajax call
        $.ajax({
            url: $el.attr('href')
        })
        .always(function(msg) {
            $el.after("<div>" + msg + "</div>")
            $el.removeClass('icon icon-spinner');
            $el.html(oldtext);
        });
    })
});