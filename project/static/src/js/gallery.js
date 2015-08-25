(function (factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['npm-zepto'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // Node/CommonJS
    module.exports = factory(require('npm-zepto'));
  } else {
    // Browser globals
    factory($);
  }
}(function ($) {

  "use strict";

  require("magnific-popup");

  var DIRECTIONS = {
    LEFT: -1,
    NONE: 0,
    RIGHT: 1,
  }

  $.fn.doScroll = function(duration, direction) {
    var target = this[0];
    var startPosition = target.scrollLeft;

    var delta;
    switch (direction) {
      case DIRECTIONS.LEFT:
        delta = -target.scrollLeft;
        break;
      case DIRECTIONS.RIGHT:
        delta = target.scrollWidth - this.width() - startPosition;
        break;
      default:
        return;
    }
    var dur = duration * (delta / target.scrollWidth);
    var startTime = Date.now();

    var performScroll = (function () {
      var fraction = Math.min(1, Math.abs((Date.now() - startTime) / dur));
      if (isNaN(fraction)) { return; } // prevent endless scrolling

      target.scrollLeft = startPosition + delta * fraction;

      if (fraction < 1 && (this.hasClass("play"))) {
        setTimeout(performScroll, 15);
      }
    }).bind(this);

    performScroll();
  }

  $(document).on("DOMContentLoaded", (function () {
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
    gallery.on("mousemove", function(e) {
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
        gallery.triggerHandler("mouseleave");
      }
    });
    gallery.on("mouseleave", function(e) {
      gallery.removeClass("play");
    });

    // Touches (a primitive crutch)
    var touchX;
    gallery.on("touchstart", function(e) {
      gallery.triggerHandler("mouseleave");  // To avoid glitches when trying both swipe and mouse
      touchX = e.changedTouches[0].clientX;
    });
    gallery.on("touchmove", function(e) {
      var diff = touchX - e.changedTouches[0].clientX;
      touchX = e.changedTouches[0].clientX;
      gallery.scrollLeft(gallery.scrollLeft() + diff);
    });
    gallery.on("touchend", function(e) {
      touchX = undefined;
    });
  }));
}));
