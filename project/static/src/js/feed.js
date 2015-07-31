var React = require('react');
//var $ = require('jquery');


var feed = React.createFactory(require('./feed/index.js'));
React.render(feed(), document.getElementById("vacancies"));
