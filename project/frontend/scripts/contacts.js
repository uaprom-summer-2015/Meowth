"use strict";
require('lodash');
var DEFAULT_PARAMS = {
    clat: 0.0,
    clng: 0.0,
    mlat: 0.0,
    mlng: 0.0,
    zoom: 0
};


document.addEventListener("DOMContentLoaded", function (event) {
    window.initializeMap = function () {
        var mapCanvas = document.getElementById("container-map");
        var params = _.transform(mapCanvas.dataset, function (result, value, key) {
            result[key] = parseFloat(value);
        });
        params = _.defaults(params, DEFAULT_PARAMS);
        var mapOptions = {
            center: new google.maps.LatLng(params.clat, params.clng),
            zoom: params.zoom,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            scrollwheel: false,
            disableDoubleClickZoom: true,
            zoomControl: true,
            scaleControl: false,
            panControl: false,
            mapTypeControl: false,
            streetViewControl: false
        };
        var map = new google.maps.Map(mapCanvas, mapOptions);
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(params.mlat, params.mlng),
            map: map
        });
    };
});
