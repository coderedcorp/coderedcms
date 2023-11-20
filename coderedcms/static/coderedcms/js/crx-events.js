/*
Wagtail CRX (https://www.coderedcorp.com/cms/)
Copyright 2018-2023 CodeRed LLC
License: https://github.com/coderedcorp/coderedcms/blob/main/LICENSE
@license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
*/

document.addEventListener("DOMContentLoaded", function () {
  var calendars = document.querySelectorAll("[data-block='calendar']");
  calendars.forEach(function (el) {
    var pageId = el.dataset.pageId; // data-page-id
    var defaultDate = el.dataset.defaultDate; // data-default-date
    var defaultView = el.dataset.defaultView; // data-default-view
    var eventDisplay = el.dataset.eventDisplay; // data-event-display
    var eventSourceUrl = el.dataset.eventSourceUrl // data-event-source-url
    var timezone = el.dataset.timezone; // data-timezone
    var calendar = new FullCalendar.Calendar(el, {
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,dayGridWeek,timeGridDay,listMonth",
      },
      themeSystem: "bootstrap5",
      buttonText: {
        prev: "← prev",
        next: "next →",
      },
      initialDate: defaultDate,
      initialView: defaultView,
      fixedWeekCount: false,
      timeZone: timezone,
      eventDisplay: eventDisplay,
      eventSources: {
        url: eventSourceUrl,
        method: "GET",
        extraParams: {
          pid: pageId,
        },
      },
    });
    calendar.render();
  });
});
/* @license-end */
