document.addEventListener("DOMContentLoaded", (function () {
    var React = require('react');
    var Gallery = require('./gallery/gallery');

    React.render(React.createElement(Gallery, null),
        document.getElementById('gallery'));
}));