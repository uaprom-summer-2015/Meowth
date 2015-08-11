var React = require('react');
var Select = require('react-select');


var option_elements = document.getElementById("block_1").getElementsByTagName("option");
var options = [];

for (var i = 0; i < option_elements.length; i++) {
    options.push({
        value: option_elements[i].getAttribute("value"),
        label: option_elements[i].innerHTML
    })
}


var PageBlockChooser = React.createClass(
    {
        displayName: "PageBlocks",
        ref: "chooser",

        getInitialState: function () {
            return {
                pageblocks: ["1", "3", "2"]
            }
        },
        addBlock: function () {
            return {pageblocks: this.state.pageblocks.concat(["1"])}
        },
        removeBlock: function (i) {
            this.setState(function (prevState) {
                var pageblocks = prevState.pageblocks.slice();
                pageblocks.splice(i, 1);
                return {pageblocks: pageblocks};
            })
        },

        render: function () {
            var self = this;

            return React.createElement("ul", null,
                this.state.pageblocks.map(function (pageblock, i) {
                    return React.createElement("div", null,
                        React.createElement(Select, {
                            inputProps: {"id": i, "name": i},
                            key: i,
                            options: options,
                            value: pageblock
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