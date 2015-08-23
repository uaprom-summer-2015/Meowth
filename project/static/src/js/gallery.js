var $ = require('npm-zepto');

$.fn.scrollToLeft = function(duration) {
    var $el = this;
    var el  = $el[0];
    var startPosition = el.scrollLeft
    var delta = el.scrollWidth - $el.width() - startPosition;
    var dur = duration * (delta / el.scrollWidth)

    var startTime = Date.now();

    function scroll() {
        var fraction = Math.min(1, (Date.now() - startTime) / dur);

        el.scrollLeft = delta * fraction + startPosition;

        if (fraction < 1 && $el.hasClass('playright'))  {
            setTimeout(scroll, 10);
        }
    }
    scroll();
};

$.fn.scrollToRight = function(duration) {
    var $el = this;
    var el  = $el[0];
    var startPosition = el.scrollLeft
    var delta = startPosition;
    var dur = duration * (delta / el.scrollWidth)

    var startTime = Date.now();

    function scroll() {
        var fraction = Math.min(1, (Date.now() - startTime) / dur);

        el.scrollLeft = startPosition - delta * fraction;

        if (fraction < 1 && $el.hasClass('playleft'))  {
            setTimeout(scroll, 10);
        }
    }
    scroll();
};


document.addEventListener("DOMContentLoaded", (function () {
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

    gal = document.getElementById('gallery');
    gal.addEventListener('mousemove', function(e) {
        if (e.screenX > window.innerWidth*0.8 && !$('#gallery').hasClass('playright')) {
            $('#gallery').removeClass('playleft');
            $('#gallery').addClass('playright');
            $('#gallery').scrollToLeft(20000);
        }
        if (e.screenX < window.innerWidth*0.2 && !$('#gallery').hasClass('playleft')) {
            $('#gallery').removeClass('playright');
            $('#gallery').addClass('playleft');
            $('#gallery').scrollToRight(20000);
        }
        if (e.screenX > window.innerWidth*0.2 && e.screenX < window.innerWidth*0.8) {
            $('#gallery').removeClass('playright playleft');
        }
    });
    gal.addEventListener('mouseleave', function(e) {
        $('#gallery').removeClass('playright playleft');
    });

}));






