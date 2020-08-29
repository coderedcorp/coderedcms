/*
CodeRed CMS (https://www.coderedcorp.com/cms/)
Copyright 2018-2019 CodeRed LLC
License: https://github.com/coderedcorp/coderedcms/blob/dev/LICENSE
@license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
*/

libs = {
    modernizr: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js",
        integrity: "sha256-0rguYS0qgS6L4qVzANq4kjxPLtvnp5nn2nB5G1lWRv4=",
    },
    moment: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.min.js",
        integrity: "sha256-4iQZ6BVL4qNKlQ27TExEhBN1HFPvAvAMbFavKKosSWQ="
    },
    pickerbase: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.6.3/compressed/picker.js",
        integrity: "sha256-hjN7Qqm7pjV+lms0uyeJBro1vyCH2azVGqyuWeZ6CFM=",
        head: '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.6.3/compressed/themes/default.css" integrity="sha256-wtVxHQXXtr975G710f51YDv94+6f6cuK49PcANcKccY=" crossorigin="anonymous" />'
    },
    pickadate: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.6.3/compressed/picker.date.js",
        integrity: "sha256-Z4OXXhjTbpFlc4Z6HqgVtVaz7Nt/3ptUKBOhxIze1eE=",
        head: '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.6.3/compressed/themes/default.date.css" integrity="sha256-U24A2dULD5s+Dl/tKvi5zAe+CAMKBFUaHUtLN8lRnKE=" crossorigin="anonymous" />'
    },
    pickatime: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.6.3/compressed/picker.time.js",
        integrity: "sha256-mvFcf2wocDC8U1GJdTVSmMHBn/dBLNeJjYRvBhM6gc8=",
        head: '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pickadate.js/3.6.3/compressed/themes/default.time.css" integrity="sha256-dtpQarv++ugnrcY7o6Gr3m7fIJFJDSx8v76jjTqEeKE=" crossorigin="anonymous" />'
    },
    jquery_ui: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.js",
        integrity: "sha256-T0Vest3yCU7pafRw9r+settMBX6JkKN06dqBnpQ8d30=",
    },
    jquery_qtip: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/qtip2/3.0.3/basic/jquery.qtip.min.js",
        integrity: "sha256-219NoyU6iEtgMGleoW1ttROUEs/sux5DplKJJQefDwE=",
    },
    fullcalendar: {
        url: "https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.10.0/fullcalendar.min.js",
        integrity: "sha256-4+rW6N5lf9nslJC6ut/ob7fCY2Y+VZj2Pw/2KdmQjR0=",
        head: '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.10.0/fullcalendar.min.css" integrity="sha256-9VgA72/TnFndEp685+regIGSD6voLveO2iDuWhqTY3g=" crossorigin="anonymous" />' +
              '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/3.10.0/fullcalendar.print.min.css" media="print" integrity="sha256-JYJWCNB1pXBwUngem7hITwB6SdmCGkhewhKS8NL1A8A=" crossorigin="anonymous" />'
    },
    coderedmaps: {
        url: "/static/coderedcms/js/codered-maps.js",
        integrity: "",
    },
    coderedstreamforms: {
        url: "/static/coderedcms/js/codered-streamforms.js",
        integrity: "",
    }
}

function load_script(lib, success) {
    // lib is an entry in `libs` above.
    // It is best to put functionality related to the script you are loading into the success callback of the load_script function.
    // Otherwise, it might not work as intended.
    if(lib.head) {
        $('head').append(lib.head);
    }
    if(lib.url){
        $.ajax({
            url: lib.url,
            dataType: "script",
            integrity: lib.integrity,
            crossorigin: "anonymous",
            success: success
        });
    }
}


$(document).ready(function()
{

    /*** AJAX Setup CSRF Setup ***/
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


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

    /*** Calendar **/
    if ( $("[data-block='calendar']").length > 0){
        load_script(libs.jquery_ui, function(){
            load_script(libs.jquery_qtip, function(){
                load_script(libs.moment, function(){
                    load_script(libs.fullcalendar, function(){
                        var pageId = "";
                        var defaultDate = "";
                        var defaultView = "";
                        $('[data-block="calendar"]').each(function(index, obj){
                            pageId = $(obj).data('page-id');
                            defaultDate = $(obj).data('default-date');
                            defaultView = $(obj).data('default-view');
                            $(obj).fullCalendar({
                                header: {
                                    left: 'prev,next,today',
                                    center: 'title',
                                    right: 'month,agendaWeek,agendaDay,listMonth'
                                },
                                defaultDate: defaultDate,
                                defaultView: defaultView,
                                fixedWeekCount: false,
                                events: {
                                    url: '/ajax/calendar/events/',
                                    type: 'GET',
                                    data: {
                                        'pid': pageId
                                    }
                                }
                            });
                        });
                    });
                });
            });
        });
    }

    if ($('#cr-map').length > 0) {
        load_script(libs.coderedmaps, function() {
            $.ajax({
                url: 'https://maps.googleapis.com/maps/api/js',
                type: "get",
                dataType: "script",
                data: {
                    'key': $("#cr-map").data( "key" ),
                    'callback': $("#cr-map").data( "callback" ),
                    'libraries': $("#cr-map").data( "libraries" ),
                }
            });
        });
    }

    if ($('.stream-form-input').length > 0){
        load_script(libs.coderedstreamforms);
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


    /*** Tracking ***/
    if(typeof cr_track_clicks !== 'undefined' && cr_track_clicks) {
        $('a').on('click', function(){
            gtag_data = {
                "event_category": "Link",
                "event_label": $(this).text().trim().substring(0, 30)
            };
            if ($(this).data('ga-event-category')) {
                gtag_data['event_category'] = $(this).data('ga-event-category');
            }
            if ($(this).data('ga-event-label')) {
                gtag_data['event_label'] = $(this).data('ga-event-label');
            }
            gtag('event', 'click', gtag_data);
        });
    }

    /*** Link handling ***/
    if(typeof cr_external_new_tab !== 'undefined' && cr_external_new_tab) {
        $('a').each(function() {
            var href = $(this).prop('href').trim();
            if(
                !href.startsWith(cr_site_url) &&
                !href.startsWith('/') &&
                !href.startsWith('#') &&
                !href.startsWith('?')
            ) {
                $(this).prop('target', '_blank');
            }
        });
    }

});

/* @license-end */
