var React = require('react');

var Image = React.createClass({
    displayName: "Image",
    render: function () {
        return (
            React.createElement("img", {
                src: this.props.src,
                className: this.props.className + " gallery-image gallery-lightbox-image img-responsive",
                onClick: this.props.onClick
            })
        );
    }
});

module.exports = Image;