var React = require('react');


var feed = React.createFactory(require('./feed/index.js'));
React.render(feed(), document.getElementById("vacancies"));
