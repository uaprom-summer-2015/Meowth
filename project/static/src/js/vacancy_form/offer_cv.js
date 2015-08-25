var React = require('react');
var ApplyForm = require('./form.js');

var VacancyDescription = React.createClass({
    render: function() {
        return (
            React.DOM.div({className: 'vacancy-desc'},
                React.DOM.h1({className: 'vacancy-title'}, 'Предложите резюме'),
                React.DOM.div({className: 'vacancy-text'},
                    React.DOM.p(null, 'Если вы не нашли нужную вакансию, но хотите у нас работать предложите нам ваше резюме и напишите чем можете быть полезны для компании Prom.ua')
                )
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
