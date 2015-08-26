var React = require('react');
var classNames = require('classnames');
var _ = require('lodash');
var $ = require('npm-zepto');

var UploadFileButton = React.createClass({

    getInitialState: function() {
        return { fileSize: '', success: false }
    },

    changeFile: function(e) {
        var error, success;
        var attachment = e.target.files[0];
        var largeSize = this.validateSize(attachment.size);
        var goodExtension = this.validateExtension(attachment.name);
        if (largeSize) {
            error = 'Файл слишком большой, попробуйте загрузить до 15 Мб';
        } else if (!goodExtension) {
            error = 'Недопустимое расширение файла';
        } else if (attachment.size == 0) {
            error = 'Нельзя прикреплять пустой файл';
        } else {
            error = '';
        }
        if (error) {
            $('#attachment').val('');
            success = false;
            this.props.handleFileName('');
        } else {
            success = true;
            this.props.handleFileName(attachment.name);
            this.setFileSize(attachment.size);
        }

        this.props.handleFileError(error);
        this.setState({ success: success});
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

    setFileSize: function(size) {
        var msg;
        var kb_in_mb = 1024;
        var units = ['байт', 'Кб','Мб'];
        var u = 0;
        while (Math.abs(size) >= kb_in_mb) {
            size /= kb_in_mb;
            u++;
        }
        msg = size.toFixed(1) + ' ' + units[u];
        this.setState({ fileSize: msg });
    },

    render: function() {
        var fileClass = classNames('form-file', {'has-error': this.props.fileError,
            'upload-file-success': this.state.success});
        var buttonClass = classNames('form-file-btn', {'btn btn-grey': !this.state.success,
            'file-success-chosen': this.state.success});
        return (
            React.DOM.div({className: fileClass},
                React.DOM.div({className: buttonClass},
                    React.DOM.input({type: "file", id: "attachment", name: "attachment",
                           onChange: this.changeFile, multiple: true, className: 'input-hidden'}),
                           'Прикрепить файл резюме'),
                React.DOM.div({className: 'file-message'},
                    React.DOM.p({className: 'file-name'}, this.props.fileName),
                    React.DOM.p({className: 'file-size'}, this.state.fileSize)
                ),
                React.DOM.p(null, this.props.fileError)
            )
        )
    }
});

var ApplyForm = React.createClass({displayName: "ApplyForm",
    getInitialState: function() {
        return { name: '', email: '', phone: '', comment: '',
                 nameError: '', emailError: '', phoneError: '', fileError: '',
                 success: false, fileName: ''}
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
    handleFileName: function(name) {
        this.setState({fileName: name});
    },
    handleFileError: function (error) {
        this.setState({fileError: error});
    },
    handleLoad: function(resp) {
        if (resp['success']) {
            this.props.handleSuccess()
        }
        this.setState({ success: resp['success'], nameError: resp['name'],
                                    emailError: resp['email'], phoneError: resp['phone'],
                                    fileError: resp['attachment']});
    },
    notFullForm: function() {
        return _.any( [!this.state.name, !this. state.email, !this.state.phone, !this.state.fileName,
            this.state.nameError, this.state.emailError,
            this.state.phoneError, this.state.fileError] )
    },
    handleSubmit: function(e) {
        e.preventDefault();
        if ( !this.notFullForm() ) {
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
        var buttonClass = classNames('btn btn-action-colored btn-apply-form', {'disabled': this.notFullForm()});
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

                React.createElement(UploadFileButton, {handleFileName: this.handleFileName,
                    handleFileError: this.handleFileError, fileName: this.state.fileName,
                    fileError: this.state.fileError}),

                React.DOM.button({className: buttonClass}, 'Отправить резюме')
            )
        );

    }
});

module.exports = ApplyForm;
