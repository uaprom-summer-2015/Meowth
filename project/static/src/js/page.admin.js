document.addEventListener("DOMContentLoaded", (function () {
var React = require('react');
var PageBlockChooser = require("./admin/page");

React.render(React.createElement(PageBlockChooser),
    document.getElementById("test"));

    }));