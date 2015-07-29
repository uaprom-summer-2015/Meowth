var React = require('react');
var node = document.getElementById('attached-form');
var csrf_token = document.getElementById('csrf_token').content;

var form = React.createFactory(require('./form_with_ajax.js'));
React.render(form({csrf_token: csrf_token}), node);
