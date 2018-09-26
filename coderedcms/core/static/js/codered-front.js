libs = {
    modernizr: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js",
        integrity: "sha256-0rguYS0qgS6L4qVzANq4kjxPLtvnp5nn2nB5G1lWRv4=",
    },
    moment: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.2/moment.min.js",
        integrity: "sha256-CutOzxCRucUsn6C6TcEYsauvvYilEniTXldPa6/wu0k="
    },
    pickerbase: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.5.6/compressed/picker.js",
        integrity: "sha256-A1y8n02GW5dvJFkEOX7UCbzJoko8kqgWUquWf9TWFS8=",
        head: '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.5.6/compressed/themes/default.css" integrity="sha256-HJnF0By+MMhHfGTHjMMD7LlFL0KAQEMyWB86VbeFn4k=" crossorigin="anonymous" />'
    },
    pickadate: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.5.6/compressed/picker.date.js",
        integrity: "sha256-rTh8vmcE+ZrUK3k9M6QCNZIBmAd1vumeuJkagq0EU3g=",
        head: '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.5.6/compressed/themes/default.date.css" integrity="sha256-Ex8MCGbDP5+fEwTgLt8IbGaIDJu2uj88ZDJgZJrxA4Y=" crossorigin="anonymous" />'
    },
    pickatime: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.5.6/compressed/picker.time.js",
        integrity: "sha256-vFMKre5X5oQN63N+oJU9cJzn22opMuJ+G9FWChlH5n8=",
        head: '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.5.6/compressed/themes/default.time.css" integrity="sha256-0GwWH1zJVNiu4u+bL27FHEpI0wjV0hZ4nSSRM2HmpK8=" crossorigin="anonymous" />'
    }
}

function load_script(lib, success) {
    // lib is an entry in `libs` above.
    if(lib.head) {
        $('head').append(lib.head);
    }
    $.ajax({
        url: lib.url,
        dataType: "script",
        integrity: lib.integrity,
        crossorigin: "anonymous",
        success: success
    });
}


$(document).ready(function()
{
    /*** Forms ***/
    if ( $('form').length > 0) {
        load_script(libs.modernizr, function() {
            if ( (!Modernizr.inputtypes.date || !Modernizr.inputtypes.time) && $("input[type='date'], input[type='time']").length > 0) {
                load_script(libs.pickerbase, function() {
                    $(document).trigger("base-picker-loaded");
                });
            }
            if(!Modernizr.inputtypes.date && $("input[type='date']").length > 0) {
                $(document).on("base-picker-loaded", function() {
                    load_script(libs.pickadate, function() {
                        // Show date picker
                        $("input[type='date']").pickadate({
                            format: 'mm/dd/yyyy',
                            selectMonths: true,
                            selectYears: true
                        });
                    });
                });
            }
            if(!Modernizr.inputtypes.time && $("[type='time']").length > 0) {
                $(document).on("base-picker-loaded", function() {
                    load_script(libs.pickatime, function() {
                        // Show time picker
                        $("input[type='time']").pickatime({
                            format: 'h:i A',
                            interval: 15
                        });
                    });
                });
            }
            if (!Modernizr.inputtypes['datetime-local'] && $("input[type='datetime-local']").length > 0) {
                load_script(libs.moment, function() {
                    // Show formatting help text
                    $('.datetime-help').show();
                    // Format input on blur
                    $("[type='datetime-local']").blur(function() {
                        var clean = $.trim($(this).val());
                        if (clean != '') {
                            clean = moment(clean).format("L LT");
                            $(this).val(clean);
                        }
                    });
                });
            }
        });
    }


    /*** Lightbox ***/
    $('.lightbox-preview').on('click', function(event) {
        var orig_src = $(this).find('img').data('original-src');
        var orig_alt = $(this).find('img').attr('alt');
        var orig_ttl = $(this).find('img').attr('title');
        var $lightbox = $($(this).data('target'));
        $lightbox.find('img').attr('src', orig_src);
        $lightbox.find('img').attr('alt', orig_alt);
        $lightbox.find('img').attr('title', orig_ttl);
    });


    /*** Content walls ***/
    $(".modal[data-cr-wall-showonce='true']").on('hide.bs.modal', function() {
        localStorage["cr_wall_" + $(this).data("cr-wall-id")] = "dismissed";
    });
    $(".modal[data-cr-wall-id]").each(function() {
        if(localStorage["cr_wall_" + $(this).data("cr-wall-id")] === undefined) {
            $(this).modal('show');
        }
    });
});