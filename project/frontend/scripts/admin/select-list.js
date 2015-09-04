var React = require('react');
var Select = require('react-select');
var $ = require('npm-zepto');

var SelectRow = React.createClass({
    displayName: "SelectRow",

    render: function () {
        return React.DOM.div({className: "select-row"},
            React.createElement(Select, {
                name: this.props.name,
                className: "select-element",
                options: this.props.options,
                value: this.props.value,
                clearable: false,
                onChange: this.props.selectOnChange
            }),
            React.DOM.a({
                className: "btn btn-default select-delete",
                onClick: this.props.deleteOnClick
            }, "Удалить")
        )
    }

});


var SelectList = React.createClass(
    {
        displayName: "SelectList",

        getInitialState: function () {
            return {currentChoices: []}
        },

        componentDidMount: function () {
            $.get(this.props.source, function (result) {
                if (this.isMounted()) {
                    this.setState({currentChoices: result.entries});
                }
            }.bind(this));
        },

        addRow: function () {
            this.setState(function () {
                return {currentChoices: this.state.currentChoices.concat(["1"])}
            });
        },
        removeRow: function (i) {
            this.setState(function (prevState) {
                var choices = prevState.currentChoices.slice();
                choices.splice(i, 1);
                return {currentChoices: choices};
            })
        },
        selectOnChange: function (el, newValue) {
            this.setState(function (prevState) {
                var choices = prevState.currentChoices.slice();
                choices[el] = newValue;
                return {currentChoices: choices};
            })
        },

        render: function () {
            return React.DOM.div( null,
                this.state.currentChoices.map(function (selectedValue, i) {
                    return React.createElement(SelectRow, {
                        key: i,
                        name: this.props.prefix + i,
                        options: this.props.options,
                        value: selectedValue,
                        selectOnChange: this.selectOnChange.bind(this, i),
                        deleteOnClick: this.removeRow.bind(this, i)
                    })
                }, this),
                React.DOM.a({
                    className: "btn btn-default",
                    onClick: this.addRow
                }, this.props.newRowTitle)
            )
        }
    }
);

module.exports = SelectList;