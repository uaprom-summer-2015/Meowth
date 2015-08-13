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
        'visible': true,
        'customComponent': LinkComponent
    },
    {
        'columnName': 'short_description',
        'visible': true,
        'displayName': 'Короткое описание'
    },
    {
        'columnName': 'hide',
        'visible': true,
        'displayName': 'Видимая',
        'customComponent': BooleanComponent
    },
    {
        'columnName': 'description',
        'visible': false
    },
    {
        'columnName': 'keywords',
        'visible': false
    },
    {
        'columnName': 'name_in_url',
        'visible': false
    },
    {
        'columnName': 'deleted',
        'visible': false
    },
    {
        'columnName': 'city_id',
        'visible': false
    },
    {
        'columnName': 'category_id',
        'visible': false
    },
    {
        'columnName': 'user_id',
        'visible': false
    },
    {
        'columnName': 'id',
        'visible': false
    },
    {
        'columnName': 'text',
        'visible': false
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
