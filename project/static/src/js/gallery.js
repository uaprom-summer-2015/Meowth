(function ($) {

  "use strict";

  var DIRECTIONS = {
    LEFT: -1,
    NONE: 0,
    RIGHT: 1,
  }

  $.fn.doScroll = function(duration, direction) {
    var $elem = this;
    var target = this[0];
    var startPosition = target.scrollLeft;

    var delta;
    switch (direction) {
      case DIRECTIONS.LEFT:
        delta = -target.scrollLeft;
        break;
      case DIRECTIONS.RIGHT:
        delta = target.scrollWidth - $elem.width() - startPosition;
        break;
      default:
        return;
    }
    var dur = duration * (delta / target.scrollWidth);
    var startTime = Date.now();

    function performScroll() {
      var fraction = Math.min(1, Math.abs((Date.now() - startTime) / dur));
      if (isNaN(fraction)) { return; } // prevent endless scrolling

      target.scrollLeft = startPosition + delta * fraction;

      if (fraction < 1 && ($elem.hasClass("play"))) {
        setTimeout(performScroll, 15);
      }
    }

    performScroll();
  }

  document.addEventListener("DOMContentLoaded", (function () {
    require("magnific-popup");
    var gallery = $("#gallery");
    gallery.magnificPopup({
      delegate: "a",
      type: "image",
      closeOnContentClick: false,
      closeBtnInside: false,
      mainClass: "mfp-with-zoom mfp-img-mobile",
      image: {
        verticalFit: true
      },
      gallery: {
        enabled: true,
        preload: [1, 1]
      }
    });
    gallery.css("overflow-x","hidden");
    gallery.css("overflow-y","hidden");
    var gal = gallery[0];
    gal.addEventListener("mousemove", function(e) {
      if (e.screenX > window.innerWidth*0.7) {
        if (! gallery.hasClass("play")) {
          gallery.addClass("play");
          gallery.doScroll(15000, DIRECTIONS.RIGHT);
        }
      } else if (e.screenX < window.innerWidth*0.3) {
        if (! gallery.hasClass("play")) {
          gallery.addClass("play");
          gallery.doScroll(15000, DIRECTIONS.LEFT);
        }
      } else {
        gallery.mouseleave();
      }
    });
    gal.addEventListener("mouseleave", function(e) {
      gallery.removeClass("play");
    });
  }));
})(require("npm-zepto"));
