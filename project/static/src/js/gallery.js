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

    $('.border').on('mouseenter', function(e) {
        console.dir(e.target);
        if (e.target.classList.contains('borderright')) {
            $('#gallery').addClass('playright');
            $('#gallery').scrollToLeft(30000);
        } else {
            $('#gallery').addClass('playleft');
            $('#gallery').scrollToRight(30000);
        }
    }).on('mouseleave', function(e) {
        if (e.target.classList.contains('borderright')) {
            $('#gallery').removeClass('playright');
        } else {
            $('#gallery').removeClass('playleft');
        }
    });

}));






