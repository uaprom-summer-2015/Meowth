var React = require('react');
var form = require('./vacancy_form/vacancy_with_form.js');


$(document).on("DOMContentLoaded", function () {
    var node = document.getElementById('vacancy-with-form');
    var csrf_token = document.getElementById('csrf_token').content;
    React.render(form({csrf_token: csrf_token}), node);
});