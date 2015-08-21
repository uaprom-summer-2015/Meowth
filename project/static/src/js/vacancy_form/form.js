var React = require('react');
var classNames = require('classnames');

var UploadFileButton = React.createClass({

    getInitialState: function() {
        return { fileName: '', fileSize: '', success: false, fileError: '' }
    },

    changeFile: function(e) {
        var error;
        var attachment = e.target.files[0];
        var largeSize = this.validateSize(attachment.size);
        var goodExtension = this.validateExtension(attachment.name);
        if (largeSize) {
            error = 'Файл слишком большой, попробуйте загрузить до 15 Мб';
        } else if (!goodExtension) {
            error = 'Недопустимое расширение файла';
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
            return ['txt', 'pdf', 'doc', 'docx', 'pptx', 'ppt', 'rtf'].indexOf(ext) != -1;
        } else {
            return false;
        }
    },

    render: function() {
        var fileClass = classNames('form-file', {'has-error': this.state.fileError,
            'upload-file-success': this.state.success});
        return (
            React.DOM.div({className: fileClass},
                React.DOM.button({className: "form-file-btn btn btn-grey"},
                    React.DOM.input({type: "file", id: "attachment", name: "attachment",
                           onChange: this.changeFile, multiple: true, className: 'input-hidden'}), 'Gh'),
                React.DOM.p(null, this.state.fileError)
            )
        )
    }
});

var ApplyForm = React.createClass({displayName: "ApplyForm",
    getInitialState: function() {
        return { name: '', email: '', phone: '', comment: '',
                 nameError: '', emailError: '', phoneError: '',
                 largeSize: false, goodExtension: true, fileError: '',
                 attachment: null, success: false, fileMessage: ''}
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
        if (largeSize) {
            error = 'Файл слишком большой, попробуйте загрузить до 15 Мб';
        } else if (!goodExtension) {
            error = 'Недопустимое расширение файла';
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
            return ['txt', 'pdf', 'doc', 'docx', 'pptx', 'ppt', 'rtf'].indexOf(ext) != -1;
        } else {
            return false;
        }
    },
    handleLoad: function(resp) {
        this.setState({ success: resp['success'], nameError: resp['name'],
                                    emailError: resp['email'], phoneError: resp['phone'],
                                    fileError: resp['attachment']});
    },
    notFull: function() {
        return (!this.state.name || !this. state.email || !this.state.phone
            || this.state.nameError || this.state.emailError
            || this.state.phoneError || this.state.fileError)
    },
    handleSubmit: function(e) {
        e.preventDefault();
        if (this.state.nameError || this.state.emailError
            || this.state.phoneError || this.state.fileError) {
        } else {
            var form = React.findDOMNode(this);
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
        var nameClass = classNames("form-name", {'has-error': this.state.nameError});
        var emailClass = classNames("form-email", {'has-error': this.state.emailError});
        var phoneClass = classNames("form-phone", {'has-error': this.state.phoneError});
        //var fileClass = classNames('form-file', {'has-error': this.state.fileError});
        var buttonClass = classNames('btn btn-action-colored', {'disabled': this.notFull()});
        if (this.state.success == false) {
            return (
                React.DOM.form({className: "apply-form", name: "ApplyForm", id: "ApplyForm",
                      onSubmit: this.handleSubmit, encType: "multipart/form-data", ref: "ApplyForm"},

                    React.DOM.input({type: "hidden", name: "csrf_token", value: this.props.csrf_token}),

                    React.DOM.div({className: nameClass},
                        React.DOM.label({htmlFor: "name"},  'Ваши имя и фамилия'),
                        React.DOM.input({name: "name", type: "text", id: "name",
                               placeholder: "Иван Иванович Иванов", value: this.state.name, onChange: this.changeName}),
                        React.DOM.p(null, this.state.nameError)
                    ), 

                    React.DOM.div({className: emailClass},
                        React.DOM.label({htmlFor: "email"}, 'Email'),
                        React.DOM.input({name: "email", type: "email", id: "email",
                               placeholder: "example@gmail.com", value: this.state.email, onChange: this.changeEmail}),
                        React.DOM.p(null, this.state.emailError)
                    ), 

                    React.DOM.div({className: phoneClass},
                        React.DOM.label({htmlFor: "phone"}, 'Контактный телефон'),
                        React.DOM.input({name: "phone", type: "text", id: "phone",
                               placeholder: "(044) 555-55-55", value: this.state.phone, onChange: this.changePhone}),
                        React.DOM.p(null, this.state.phoneError)
                    ), 

                    React.DOM.div({className: "form-comment"},
                        React.DOM.label({htmlFor: "comment"}, 'Сопроводительный текст'),
                        React.DOM.textarea({name: "comment", id: "comment"})
                    ),


                    //React.DOM.div({className: fileClass},
                    //    React.DOM.button({className: "form-file-btn btn btn-grey"},
                    //        React.DOM.input({type: "file", id: "attachment", name: "attachment",
                    //               onChange: this.changeFile, multiple: true, className: 'input-hidden'}),
                    //        'Прикрепить файл резюме'),
                    //    React.DOM.p(null, this.state.fileError)
                    //),

                    React.DOM.input({type: "submit", value: 'Отправить резюме', className: buttonClass})
                )
            );
        } else {
            return (
                React.DOM.h2(null, "Success")
            );
        }
    }
});

module.exports = React.createFactory(ApplyForm);
