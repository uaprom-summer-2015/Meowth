(function (factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['lodash'], factory);
    } else if (typeof module === 'object' && module.exports) {
        // Node/CommonJS
        module.exports = factory(require('lodash'));
    } else {
        // Browser globals
        factory(_);
    }
}(function (_) {
  "use strict";

  var DEFAULT_PARAMS = {
    clat: 0.0,
    clng: 0.0,
    mlat: 0.0,
    mlng: 0.0,
    zoom: 0,
  }

  window.initializeMap = function() {
    var mapCanvas = document.getElementById("container-map");
    var params = _.transform(mapCanvas.dataset, function(result, value, key) {
        result[key] = parseFloat(value);
    });
    params = _.defaults(params, DEFAULT_PARAMS);
    var mapOptions = {
      center: new google.maps.LatLng(params.clat, params.clng),
      zoom: params.zoom,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      disableDefaultUI: true,
      scrollwheel: false,
      disableDoubleClickZoom: true,
    }
    var map = new google.maps.Map(mapCanvas, mapOptions);
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(params.mlat, params.mlng),
      map: map,
    });
  }
}));
