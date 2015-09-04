var React = require('react');
var table = require('./vacancies_table/table.js');


document.addEventListener("DOMContentLoaded", (function () {
    var node = document.getElementById('id_table');

    React.render(table(), node);
}))
