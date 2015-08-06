var React = require('react');
var Image = require("./image");

var LightBox = React.createClass({
    displayName: "LightBox",
    getInitialState: function () {
        return {focused: 0};
    },
    changeSlide: function (index) {
        this.setState({focused: index})
    },
    prev: function () {
        this.changeSlide(
            this.state.focused <= 0 ?
            this.props.images.length - 1 : this.state.focused - 1
        );
    },
    next: function () {
        this.changeSlide(
            this.state.focused >= this.props.images.length - 1 ?
                0 : this.state.focused + 1
        );
    },

    render: function () {

        var self = this;
        var imageNodes = this.props.images.map(function (image, index) {
            var style = "";

            if (self.state.focused == index) {
                style = 'gallery-lightbox-focused';
            }

            return (
                React.createElement(Image, {
                    key: image.key,
                    src: image.src,
                    className: style + " center-block",
                    onClick: self.next
                })
            );
        });

        return (
            React.createElement("div", {
                    id: "gallery-lightbox",
                    className: "modal fade",
                    tabIndex: "-1",
                    role: "dialog"

                },
                React.createElement("div", {className: "modal-dialog  modal-lg"},
                    React.createElement("div", {className: "modal-content"},
                        React.createElement("div", {className: "modal-body"},
                            imageNodes
                        ),

                        React.createElement("div", {className: "modal-footer"},

                            React.createElement("button", {
                                    type: "button",
                                    className: "btn btn-default pull-left prev",
                                    onClick: self.prev
                                },
                                React.createElement("i", {className: "glyphicon glyphicon-chevron-left"},
                                    "Previous"
                                )
                            ),
                            React.createElement("button", {
                                    type: "button",
                                    className: "btn btn-primary next",
                                    onClick: self.next
                                },
                                "Next",
                                React.createElement("i", {className: "glyphicon glyphicon-chevron-right"})
                            )
                        )
                    )
                )
            )
        )
    }
});

module.exports = LightBox;