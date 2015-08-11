var React = require('react');
var Select = require('react-select');


var option_elements = document.getElementById("block_1").getElementsByTagName("option");
var options = [];

for (var i = 0; i < option_elements.length; i++) {
    var e = option_elements[i];
    options.push({
        value: e.getAttribute("value"),
        label: e.innerHTML
    });
}

var PageBlockChooser = React.createClass(
    {
        displayName: "PageBlocks",
        ref: "chooser",
        elPrefix: "block_",

        getInitialState: function () {
            var selects = document.getElementsByTagName("select");
            var pageblocks = [];

            for (var i = 0; i < selects.length; i++) {
                var e = selects[i];

                pageblocks.push(
                    e.options[e.selectedIndex].value
                );
            }
            return {
                pageblocks: pageblocks
            }
        },
        addBlock: function () {
            this.setState(function () {
                return {pageblocks: this.state.pageblocks.concat(["1"])}
            });
        },
        removeBlock: function (i) {
            this.setState(function (prevState) {
                var pageblocks = prevState.pageblocks.slice();
                pageblocks.splice(i, 1);
                return {pageblocks: pageblocks};
            })
        },
        selectOnChange: function (el, newValue) {
            this.setState(function (prevState) {
                var pageblocks = prevState.pageblocks.slice();
                pageblocks[el] = newValue;
                return {pageblocks: pageblocks};
            })
        },

        render: function () {
            var self = this;
            return React.createElement("ul", null,
                this.state.pageblocks.map(function (selectedValue, i) {
                    // TODO: fix i and index in wtforms (should starts from 0)
                    var index = i+1;
                    return React.createElement("div", null,
                        React.createElement(Select, {
                            name: self.elPrefix+index,
                            key: index,
                            options: options,
                            value: selectedValue,
                            onChange: self.selectOnChange.bind(self, i)
                        }),
                        React.createElement("div", {
                            onClick: self.removeBlock.bind(self, i)
                        }, "Delete me")
                    )
                }),
                React.createElement("div", {onClick: this.addBlock}, "Click")
            )
        }
    }
);

module.exports = PageBlockChooser;