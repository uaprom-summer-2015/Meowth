var React = require('react');
var PageBlockList = require("./admin/select-list");
var $ = require('npm-zepto');

document.addEventListener("DOMContentLoaded", (function () {
    $.get("/admin/pages/available_blocks/", function (result) {
        React.render(React.createElement(PageBlockList, {
                prefix: "blocks-",
                newRowTitle: "Добавить новый блок",
                source: "block_list/",
                options: result.blocks
            }),
            document.getElementById("container-blocks"));
    });
}));
