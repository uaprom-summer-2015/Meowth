document.addEventListener("DOMContentLoaded", (function () {
    var React = require('react');
    var PageBlockList = require("./admin/select-list");

    function parseChoices() {
        var selects = document.getElementsByTagName("select");
        var pageblocks = [];

        for (var i = 0; i < selects.length; i++) {
            var e = selects[i];

            pageblocks.push(
                e.options[e.selectedIndex].value
            );
        }
        return pageblocks
    }

    function parseOptions(){
        var option_elements = document.getElementById("blocks-0").getElementsByTagName("option");
        var options = [];

        for (var i = 0; i < option_elements.length; i++) {
            var e = option_elements[i];
            options.push({
                value: e.getAttribute("value"),
                label: e.innerHTML
            });
        }
        return options
    }

    React.render(React.createElement(PageBlockList, {
            prefix: "blocks-",
            currentChoices: parseChoices(),
            newRowTitle: "Добавить новый блок",
            options: parseOptions()
        }),
        document.getElementById("blocks"));
}));