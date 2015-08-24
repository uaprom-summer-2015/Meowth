(function () {
  "use strict";

  var DEFAULT_PARAMS = {
    clat: 0,
    clng: 0,
    mlat: 0,
    mlng: 0,
    zoom: 0,
  }

  function initialize() {
    var mapCanvas = document.getElementById('container-map');
    var params = {}
    for (var key in DEFAULT_PARAMS) {
      params[key] = parseFloat(mapCanvas.getAttribute(key)) || DEFAULT_PARAMS[key];
    }
    var mapOptions = {
      center: new google.maps.LatLng(params.clat, params.clng),
      zoom: params.zoom,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      disableDefaultUI: true,
    }
    var map = new google.maps.Map(mapCanvas, mapOptions);
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(params.mlat, params.mlng),
      map: map,
    });
  }
  google.maps.event.addDomListener(window, 'load', initialize);
})();
