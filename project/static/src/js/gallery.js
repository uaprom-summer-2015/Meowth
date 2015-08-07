document.addEventListener("DOMContentLoaded", (function () {
    $ = jQuery = require('jquery');
    require('magnific-popup');
    $('#gallery').magnificPopup({
        delegate: 'a',
        type: 'image',
        closeOnContentClick: false,
        closeBtnInside: false,
        mainClass: 'mfp-with-zoom mfp-img-mobile',
        image: {
            verticalFit: true
        },
        gallery: {
            enabled: true,
            preload: [1, 1]
        }
    });
}));