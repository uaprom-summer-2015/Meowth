var React = require('react');
var $ = require('jquery');


var feed = React.createFactory(require('./feed.jsx'));
React.render(feed(), document.getElementById("vacancies"));
