var React = require('react');
var Griddle = require('griddle-react');
var $ = require('npm-zepto');
var classNames=require('classnames');

var LinkComponent = React.createClass({
    render: function () {
        return React.DOM.a({href: '/admin/vacancy/' + this.props.rowData.id}, this.props.data)
    }
})

var BooleanComponent = React.createClass({
    render: function () {
        var className = classNames({
            'glyphicon': true,
            'glyphicon-ok': !this.props.data,
            'glyphicon-remove': this.props.data
        })
        return React.DOM.span({className: className, style:{marginLeft: '30px'}})
    }
})


var columnMeta = [
    {
        'columnName': 'title',
        'order': 1,
        'displayName': 'Название',
        'locked': true,
        'customComponent': LinkComponent
    },
    {
        'columnName': 'short_description',
        'displayName': 'Короткое описание'
    },
    {
        'columnName': 'hide',
        'displayName': 'Видимая',
        'customComponent': BooleanComponent
    },
    {
        'columnName': 'salary',
        'displayName': 'ЗП'
    },
    {
        'columnName': 'category',
        'displayName': 'Категория'
    },
    {
        'columnName': 'city',
        'displayName': 'Город'
    },
    {
        'columnName': 'updated_at',
        'displayName': 'Когда обновлена'
    },
    {
        'columnName': 'username',
        'displayName': 'Кем обновлена'
    },
    {
        'columnName': 'visits',
        'displayName': 'Количество посещений'
    },
    {
        'columnName': 'id',
        'visible': false
    },
];


var Table = React.createClass({

    getInitialState: function() {
        return { data: {} }
    },

    componentDidMount: function() {
        $.get(
            'list',
            function(result) {
                this.setState({ data: result['vacancies'] })
            }.bind(this)
        )
    },

    render: function() {
        return (
            React.createElement(Griddle, {results: this.state.data,
                showSettings: true, showFilter: true, columnMetadata: columnMeta,
                columns: ['title', 'short_description', 'hide',
                    'category', 'city', 'salary', 'visits'], resultsPerPage: 10})
        )
    }

})


module.exports = React.createFactory(Table);
