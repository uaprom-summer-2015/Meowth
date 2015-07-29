var React = require('react');
var classNames = require('classnames');

var ApplyForm = React.createClass({displayName: "ApplyForm",
    getInitialState: function() {
        return { name: '', email: '', phone: '', comment: '',
                 nameError: '', emailError: '', phoneError: '',
                 largeSize: false, goodExtension: true, fileError: '',
                 attachment: null, success: false}
    },
    changeName: function(e) {
        this.setState({ name: e.target.value, nameError: '' });
    },
    changeEmail: function(e) {
        this.setState({ email: e.target.value, emailError: '' });
    },
    changePhone: function(e) {
        this.setState({ phone: e.target.value, phoneError: '' });
    },
    changeComment: function(e) {
        this.setState({ comment: e.target.value });
    },
    changeFile: function(e) {
        var error;
        var attachment = e.target.files[0];
        var largeSize = this.validateSize(attachment.size);
        var goodExtension = this.validateExtension(attachment.name);
        if (largeSize && !goodExtension) {
            error = 'Слишком большой файл (макс 15 Мб). Недопустимое расширение файла.';
        } else if (largeSize) {
            error = 'Слишком большой файл (макс 15 Мб).';
        } else if (!goodExtension) {
            error = 'Недопустимое расширение файла.';
        } else {
            error = '';
        }

        this.setState({ largeSize: largeSize, goodExtension: goodExtension,
                        fileError: error, attachment: attachment.file});
    },
    validateSize: function(size) {
        return size > 15 * 1024 * 1024;
    },
    validateExtension: function(name) {
        if ( name.indexOf('.') != -1 ) {
            var lst = name.split('.');
            var ext = lst[lst.length - 1];
            return ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'].indexOf(ext) != -1;
        } else {
            return false;
        }
    },
    handleLoad: function(resp) {
        this.setState({ success: resp['success'], nameError: resp['name'],
                                    emailError: resp['email'], phoneError: resp['phone'],
                                    fileError: resp['attachment']});
    },
    handleSubmit: function(e) {
        e.preventDefault();
        if (this.state.nameError || this.state.emailError
            || this.state.phoneError || this.state.fileError) {
            alert('Исправьте форму');
        } else {
            var form = React.findDOMNode(this.refs.ApplyForm)
            var formData = new FormData(form);
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange=function() {
                if (xhr.readyState==4 && xhr.status==200)
                {
                    this.handleLoad(JSON.parse(xhr.responseText));
                }
            }.bind(this);
            xhr.open("POST", "form", true);
            xhr.send(formData);
        }
    },
    render: function() {
        var nameClass = classNames("form-group", {'has-error': this.state.nameError})
        var emailClass = classNames("form-group", {'has-error': this.state.emailError})
        var phoneClass = classNames("form-group", {'has-error': this.state.phoneError})
        if (this.state.success == false) {
            return (
                React.DOM.form({className: "form-horizontal", action: "form", name: "ApplyForm", id: "ApplyForm",
                      onSubmit: this.handleSubmit, encType: "multipart/form-data", ref: "ApplyForm"}, 

                    React.DOM.input({type: "hidden", name: "csrf_token", value: this.props.csrf_token}),

                    React.DOM.div({className: nameClass},
                        React.DOM.label({className: "control-label", htmlFor: "name"},  this.state.nameError),
                        React.DOM.input({name: "name", type: "text", className: "form-control", id: "name",
                               placeholder: "Имя", value: this.state.name, onChange: this.changeName})
                    ), 

                    React.DOM.div({className: emailClass},
                        React.DOM.label({className: "control-label", htmlFor: "email"},  this.state.emailError),
                        React.DOM.input({name: "email", type: "email", className: "form-control", id: "email",
                               placeholder: "Email", value: this.state.email, onChange: this.changeEmail})
                    ), 

                    React.DOM.div({className: phoneClass},
                        React.DOM.label({className: "control-label", htmlFor: "phone"},  this.state.phoneError),
                        React.DOM.input({name: "phone", type: "text", className: "form-control", id: "phone",
                               placeholder: "Телефон", value: this.state.phone, onChange: this.changePhone})
                    ), 

                    React.DOM.div({className: "form-group"},
                        React.DOM.textarea({name: "comment", id: "comment", className: "form-control",
                                  placeholder: "Коментарий"})
                    ), 

                    React.DOM.div({className: "form-group"},
                        React.DOM.label({htmlFor: "inputFile"}, "Резюме"),
                        React.DOM.input({type: "file", id: "attachment", name: "attachment",
                               onChange: this.changeFile, multiple: true}),
                        React.DOM.div({className: "has-error"},
                            React.DOM.p({className: "help-block"}, this.state.fileError)
                        )
                    ), 

                    React.DOM.input({type: "submit"})
                )
            );
        } else {
            return (
                React.DOM.h2(null, "Success")
            );
        }
    }
})

module.exports = React.createFactory(ApplyForm);
