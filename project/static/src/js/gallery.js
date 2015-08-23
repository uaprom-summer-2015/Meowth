var $ = require('npm-zepto');

$.fn.scrollToRight = function(duration) {
    var $el = this;
    var el  = $el[0];
    var startPosition = el.scrollLeft
    var delta = el.scrollWidth - $el.width() - startPosition;
    var dur = duration * (delta / el.scrollWidth)

    var startTime = Date.now();

    function scroll() {
        var fraction = Math.min(1, (Date.now() - startTime) / dur);
        if (isNaN(fraction)) { return; }

        el.scrollLeft = startPosition + delta * fraction;

        if (fraction < 1 && $el.hasClass('playright'))  {
            setTimeout(scroll, 15);
        }
    }
    scroll();
};

$.fn.scrollToLeft = function(duration) {
    var $el = this;
    var el  = $el[0];
    var startPosition = el.scrollLeft
    var delta = startPosition;
    var dur = duration * (delta / el.scrollWidth)

    var startTime = Date.now();

    function scroll() {
        var fraction = Math.min(1, (Date.now() - startTime) / dur);
        if (isNaN(fraction)) { return; }

        el.scrollLeft = startPosition - delta * fraction;

        if (fraction < 1 && $el.hasClass('playleft'))  {
            setTimeout(scroll, 15);
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
    $("#gallery").css("overflow-x","hidden");
    $("#gallery").css("overflow-y","hidden");
    gal = document.getElementById('gallery');
    gal.addEventListener('mousemove', function(e) {
        if (e.screenX > window.innerWidth*0.66) {
            $('#gallery').removeClass('playleft');
            $('#gallery').addClass('playright');
            $('#gallery').scrollToRight(15000);
        } else if (e.screenX < window.innerWidth*0.33) {
            $('#gallery').removeClass('playright');
            $('#gallery').addClass('playleft');
            $('#gallery').scrollToLeft(15000);
        } else {
            $('#gallery').removeClass('playright playleft');
        }
    });
    gal.addEventListener('mouseleave', function(e) {
        $('#gallery').removeClass('playright playleft');
    });

}));
