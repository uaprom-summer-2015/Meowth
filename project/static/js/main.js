var React = require('react');
var $ = require('jquery');

var feed = React.createFactory(require('./feed.jsx')); // need to specify the jsx extension
React.render(feed(), document.body);