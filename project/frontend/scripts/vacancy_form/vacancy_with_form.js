var React = require('react');
var $ = require('npm-zepto');
var ApplyForm = require('./form.js');

var VacancyDescription = React.createClass({
    getInitialState: function() {
        return { title: '', city: '', salary: '', text: ''}
    },

    componentDidMount: function() {
        $.get('json', function(result) {
            this.setState(result['vacancy']);
        }.bind(this));
    },

    render: function() {
        return (
            React.DOM.div({className: 'vacancy-desc'},
                React.DOM.h1({className: 'vacancy-title'}, this.state.title),
                React.DOM.p({className: 'vacancy-city'}, this.state.city),
                React.DOM.h2({className: 'vacancy-salary'}, this.state.salary),
                React.DOM.h3(null, 'Описание вакансии'),
                React.DOM.div({className: 'vacancy-text', dangerouslySetInnerHTML: {__html: this.state.text}}),
                React.DOM.h3(null, 'Отправить резюме')
            )
        );
    }
});

var Vacancy = React.createClass({
    getInitialState: function() {
        return {success: false}
    },

    handleSuccess: function () {
        this.setState({success: true})
    },

    render: function() {
        if (this.state.success) {
            return (
                React.DOM.div(null,
                    React.DOM.h1(null, "Спасибо, Ваше резюме отправлено"),
                    React.DOM.p(null, 'Мы ознакомимся с Вашим резюме и обязательно свяжемся в ближайшее время')
                )
            );
        } else {
            return (
                React.DOM.div({className: 'vacancy'},
                    React.createElement(VacancyDescription),
                    React.createElement(ApplyForm, {handleSuccess: this.handleSuccess, csrf_token: this.props.csrf_token})
                )
            )
        }
    }
});

module.exports = React.createFactory(Vacancy);
