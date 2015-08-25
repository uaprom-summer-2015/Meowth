var React = require('react');
var node = document.getElementById('vacancy-with-form');
var csrf_token = document.getElementById('csrf_token').content;

var form = require('./vacancy_form/vacancy_with_form.js');
React.render(form({csrf_token: csrf_token}), node);
