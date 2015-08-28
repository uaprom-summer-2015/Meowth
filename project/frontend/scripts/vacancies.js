var React = require('react');

var feed = React.createFactory(require('./feed/index.js'));

$(document).on("DOMContentLoaded", function () {
    React.render(feed(), document.getElementById("vacancies"));
});
