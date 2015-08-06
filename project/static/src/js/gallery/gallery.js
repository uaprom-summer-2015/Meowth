$ = jQuery = require('jquery');
var React = require('react');
var bootstrap = require('bootstrap');
var LightBox = require("./lightbox");


var Gallery = React.createClass({
    displayName: "Gallery",
    getDefaultProps: function () {
        // FIXME: hardcoded element
        var orig_images = document.getElementById('gallery').getElementsByTagName('a');

        var react_images = [];

        // parse orig_images because of  HTMLCollection.map() lack
        for (var i = 0; i < orig_images.length; i++) {
            react_images.push({
                key: i,
                full: orig_images[i].getAttribute('href'),
                thumbnail: orig_images[i].getElementsByTagName("img")[0].getAttribute("src")
            })
        }

        return {images: react_images}
    },

    handleClick: function (index) {
        this.refs.lightbox.changeSlide(index);
        $('#gallery-lightbox').modal();
    },
    render: function () {
        var self = this;

        var images = this.props.images.map(function (image) {
            return React.createElement("img", {
                key: image.key,
                src: image.thumbnail,
                className: "gallery-image",
                onClick: self.handleClick.bind(self, image.key)
            })
        });

        var full_imgs = this.props.images.map(function (image) {
            return {src: image.full, key: image.key}
        });

        return (
            React.createElement("div", null,
                React.createElement(LightBox, {
                    images: full_imgs,
                    ref: "lightbox"
                }),
                images)
        );
    }
});

module.exports = Gallery;