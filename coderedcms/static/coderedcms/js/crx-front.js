/*
Wagtail CRX (https://www.coderedcorp.com/cms/)
Copyright 2018-2023 CodeRed LLC
License: https://github.com/coderedcorp/coderedcms/blob/main/LICENSE
@license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
*/

/**
 * Main script which is used to detect CRX features requiring JavaScript.
 *
 * Loads the necessary libraries for that feature, then initializes any
 * feature-specific code. This should only be used for features that might be
 * site-wide (e.g. StreamField blocks that could occur anywhere). For
 * functionality that is page-specific, include the JavaScript normally via a
 * script tag on that page instead.
 *
 * This file must run with "pure" JavaScript - assume jQuery or any other
 * scripts are not yet loaded.
 */
const libs = {
  masonry: {
    url: "https://cdn.jsdelivr.net/npm/masonry-layout@4.2.2/dist/masonry.pkgd.min.js",
    integrity: "sha256-Nn1q/fx0H7SNLZMQ5Hw5JLaTRZp0yILA/FRexe19VdI=",
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
      referrerPolicy: "origin",
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

  /** Film Strip Controls **/
  let strips = document.querySelectorAll("[data-block='film-strip']");
  strips.forEach((el) => {
    const leftButton = el.querySelector("[data-button='left']");
    const rightButton = el.querySelector("[data-button='right']");
    const container = el.querySelector("[data-block='film-container']");

    leftButton.addEventListener("click", function () {
      const panels = el.querySelectorAll("[data-block='film-panel']");
      let currentBlock = parseInt(el.dataset.currentBlock) - 1;
      if (currentBlock < 0) currentBlock = panels.length - 1;
      el.dataset.currentBlock = currentBlock;

      const elem = panels[currentBlock];
      const left = elem.offsetLeft;

      container.scroll({ top: 0, left: left, behavior: "smooth" });
    });

    rightButton.addEventListener("click", function () {
      const panels = el.querySelectorAll("[data-block='film-panel']");
      let currentBlock = parseInt(el.dataset.currentBlock) + 1;
      if (currentBlock >= panels.length) currentBlock = 0;
      el.dataset.currentBlock = currentBlock;

      const elem = panels[currentBlock];
      const left = elem.offsetLeft;

      container.scroll({ top: 0, left: left, behavior: "smooth" });
    });
  });
});
/* @license-end */
