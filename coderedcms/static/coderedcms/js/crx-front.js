/*
Wagtail CRX (https://www.coderedcorp.com/cms/)
Copyright 2018-2022 CodeRed LLC
License: https://github.com/coderedcorp/coderedcms/blob/dev/LICENSE
@license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
*/

/**
 * Main script which is used to detect CRX features requiring JavaScript.
 *
 * Loads the necessary libraries for that feature, then initializes any
 * feature-specific code.
 *
 * This file must run with "pure" JavaScript - assume jQuery or any other
 * scripts are not yet loaded.
 */
const libs = {
  jquery: {
    url: "https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js",
    integrity: "sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=",
  },
  masonry: {
    url: "https://cdn.jsdelivr.net/npm/masonry-layout@4.2.2/dist/masonry.pkgd.min.js",
    integrity: "sha256-Nn1q/fx0H7SNLZMQ5Hw5JLaTRZp0yILA/FRexe19VdI=",
  },
  fullcalendar: {
    url: "https://cdn.jsdelivr.net/npm/fullcalendar@5.11.2/main.min.js",
    integrity: "sha256-sR+oJaZ3c0FHR6+kKaX1zeXReUGbzuNI8QTKpGHE0sg=",
    head: '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fullcalendar@5.11.2/main.min.css" integrity="sha256-5veQuRbWaECuYxwap/IOE/DAwNxgm4ikX7nrgsqYp88=" crossorigin="anonymous">',
  },
  coderedmaps: {
    url: "/static/coderedcms/js/crx-maps.js?v=" + cr_version,
    integrity: "",
  },
  coderedstreamforms: {
    url: "/static/coderedcms/js/crx-streamforms.js?v=" + cr_version,
    integrity: "",
  },
};

/**
 * Dynamically loads a script and/or CSS from the `lib` object above.
 *
 * Put functionality related to the script you are loading into the `success`
 * callback of the `load_script` function. Otherwise, it might not work as
 * intended.
 */
function load_script(lib, success) {
  var head = document.getElementsByTagName("head")[0];
  if (lib.head) {
    // Create a temporary element and insert the `lib.head` string to form a
    // child element.
    var tmpEl = document.createElement("div");
    tmpEl.innerHTML = lib.head;
    // Append the child element to the `<head>`
    head.append(tmpEl.firstElementChild);
  }
  if (lib.url) {
    // Fetch and execute the script in the global context.
    // Then call the `success` callback.
    fetch(lib.url, {
      integrity: lib.integrity,
      referrerPolicy: "no-referrer",
    })
      .then(function (response) {
        return response.text();
      })
      .then(function (txt) {
        // Eval in the global scope.
        eval?.(txt);
      })
      .then(function () {
        if (success) {
          success();
        }
      });
  }
}

document.addEventListener("DOMContentLoaded", function () {
  /** Calendar **/
  if (document.querySelectorAll("[data-block='calendar']").length > 0) {
    load_script(libs.fullcalendar, function () {
      var calendars = document.querySelectorAll("[data-block='calendar']");
      calendars.forEach(function (el) {
        var pageId = el.dataset.pageId; // data-page-id
        var defaultDate = el.dataset.defaultDate; // data-default-date
        var defaultView = el.dataset.defaultView; // data-default-view
        var eventDisplay = el.dataset.eventDisplay; // data-event-display
        var timezone = el.dataset.timezone; // data-timezone
        var calendar = new FullCalendar.Calendar(el, {
          headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay,listMonth",
          },
          themeSystem: "bootstrap",
          bootstrapFontAwesome: false,
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
            url: "/ajax/calendar/events/",
            method: "GET",
            extraParams: {
              pid: pageId,
            },
          },
        });
        calendar.render();
      });
    });
  }

  /** Location Pages (Google Maps) **/
  if (document.querySelector("#cr-map")) {
    load_script(libs.coderedmaps, function () {
      var map = document.querySelector("#cr-map");
      fetch(
        "https://maps.googleapis.com/maps/api/js?" +
          new URLSearchParams({
            key: map.dataset.key, // data-key
            callback: map.dataset.callback, // data-callback
            libraries: map.dataset.libraries, // data-libraries
          })
      );
    });
  }

  /** StreamForms **/
  if (document.querySelectorAll(".stream-form-input").length > 0) {
    load_script(libs.jquery, function () {
      load_script(libs.coderedstreamforms);
    });
  }

  /** Lightbox **/
  document.querySelectorAll(".lightbox-preview").forEach(function (el) {
    el.addEventListener("click", function (event) {
      var el = event.currentTarget;
      var orig_src = el.querySelector("img").dataset.originalSrc;
      var orig_alt = el.querySelector("img").alt;
      var orig_ttl = el.querySelector("img").title;
      var lightbox = document.querySelector(el.dataset.bsTarget);
      lightbox.querySelector("img").setAttribute("src", orig_src);
      lightbox.querySelector("img").setAttribute("alt", orig_alt);
      lightbox.querySelector("img").setAttribute("title", orig_ttl);
    });
  });

  /** Content walls **/
  document
    .querySelectorAll(".modal[data-cr-wall-showonce='true']")
    .forEach(function (el) {
      el.addEventListener("hide.bs.modal", function () {
        localStorage["cr_wall_" + el.dataset.crWallId] = "dismissed";
      });
    });
  document.querySelectorAll(".modal[data-cr-wall-id]").forEach(function (el) {
    if (localStorage["cr_wall_" + el.dataset.crWallId] === undefined) {
      const modal = new bootstrap.Modal(el);
      modal.show();
    }
  });

  /** Tracking **/
  if (typeof cr_track_clicks !== "undefined" && cr_track_clicks) {
    document.querySelectorAll("a").forEach(function (el) {
      el.addEventListener("click", function (event) {
        var el = event.currentTarget;
        gtag_data = {
          event_category: "Link",
          event_label: el.textContent.trim().substring(0, 30),
        };
        if (el.dataset.gaEventCategory) {
          gtag_data["event_category"] = el.dataset.gaEventCategory;
        }
        if (el.dataset.gaEventLabel) {
          gtag_data["event_label"] = el.dataset.gaEventLabel;
        }
        gtag("event", "click", gtag_data);
      });
    });
  }

  /** Link handling **/
  if (typeof cr_external_new_tab !== "undefined" && cr_external_new_tab) {
    document.querySelectorAll("a").forEach(function (el) {
      var href = el.href.trim();
      if (
        !href.startsWith(cr_site_url) &&
        !href.startsWith("/") &&
        !href.startsWith("#") &&
        !href.startsWith("?")
      ) {
        el.setAttribute("target", "_blank");
      }
    });
  }

  /** Masonry **/
  if (document.querySelectorAll("[data-masonry]").length > 0) {
    load_script(libs.masonry);
  }
});

/* @license-end */
