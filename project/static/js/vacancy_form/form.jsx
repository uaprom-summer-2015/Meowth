var NameInput = React.createClass({
    getInitialState: function() {
        return { name: '', success: false, show: this.props.show,
                 error: ''}
    },
    changeName: function(e) {
        this.setState({ name: e.target.value });
        var error
        if (e.target.value) {
            error = '';
            this.setState({ success: true });
        } else {
            error = 'Поле не дожно быть пустым';
            this.setState({ success: false });
        }
        this.setState({ error: error })
        this.props.registerError('Имя', error)
    },
    render: function() {
        var divClass = "form-group" + (this.state.success ? ' has-success' : '')
        var labelError = ''
        if (this.state.show) {
            labelError = this.state.error
            divClass = "form-group" + (labelError ? ' has-error' : (this.state.success ? ' has-success' : ''))
        }
        return (
            <div className={divClass}>
              <label className="control-label" htmlFor="name">{labelError}</label>
              <input name='name' type="text" className="form-control" id="name"
                     placeholder="Имя" value={this.state.name} onChange={this.changeName} />
            </div>
        )
    }
})

var EmailInput = React.createClass({
    getInitialState: function() {
        return { email: '', labelError: '', success: false, error: '' }
    },
    changeEmail: function(e) {
        var email = e.target.value
        var error, success
        if (/.+@.+\..+/.test(email)) {
            error = '';
            success = true;
        } else {
            error = 'Не корректный email'
            success = false;
        }
        this.props.registerError('Email', error)
        this.setState({ email: email, error: error, success: success });
        this.delayedCallback(email, error)

    },
    componentWillMount: function () {
        this.delayedCallback = _.debounce(function (email, error) {
            var labError = email ? error : ''
            this.setState({ labelError: labError })
        }, 500);
    },
    render: function() {
        var divClass = "form-group" + (this.state.labelError ? ' has-error' : (this.state.success ? ' has-success' : ''))
        return (
            <div className={divClass}>
                  <label className="control-label" htmlFor="email">{this.state.labelError}</label>
                  <input name='email' type="email" className="form-control" id="email"
                         placeholder="Email" value={this.state.email} onChange={this.changeEmail} />
            </div>
        )
    }
})

var PhoneInput = React.createClass({
    getInitialState: function() {
        return { phone: '', labelError: '', success: false, error: '' }
    },
    changePhone: function(e) {
        var phone = e.target.value
        var error, success

        if (/^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/.test(phone)) {
            error = '';
            success = true;
        } else {
            error = 'Не корректный номер телефона';
            success = false;
        }
        this.props.registerError('Телефон', error)
        this.setState({ phone: phone, error: error, success: success })
        this.delayedCallback(phone, error)
    },
    componentWillMount: function () {
        this.delayedCallback = _.debounce(function (phone, error) {
            var labError = phone ? error : ''
            this.setState({ labelError: labError })
        }, 500);
    },
    render: function() {
        var divClass = "form-group" + (this.state.labelError ? ' has-error' : (this.state.success ? ' has-success' : ''))
        return (
            <div className={divClass}>
                  <label className="control-label" htmlFor="phone">{this.state.labelError}</label>
                  <input name='phone' type="text" className="form-control" id="phone"
                         placeholder="Телефон" value={this.state.phone} onChange={this.changePhone} />
            </div>
        )
    }
})

var FileInput = React.createClass({
    getInitialState: function() {
        return { largeSize: false, goodExtension: true, error: '' }
    },
    changeFile: function(e) {
        var error
        largeSize = this.validateSize(e.target.files[0].size)
        goodExtension = this.validateExtension(e.target.files[0].name)
        if (largeSize && !goodExtension) {
            error = 'Слишком большой файл (макс 15 Мб). Недопустимое расширение файла.'
        } else if (largeSize) {
            error = 'Слишком большой файл (макс 15 Мб).'
        } else if (!goodExtension) {
            error = 'Недопустимое расширение файла.'
        } else {
            error = ''
        }
        this.props.registerError('File', error)
        this.setState({ largeSize: largeSize, goodExtension: goodExtension,
                        error: error})
    },
    validateSize: function(size) {
        return size > 15 * 1024 * 1024
    },
    validateExtension: function(name) {
        if ( name.indexOf('.') != -1 ) {
            lst = name.split('.')
            ext = lst[lst.length - 1]
            return ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'].indexOf(ext) != -1
        } else {
            return false
        }
    },
    render: function() {
        return (
            <div className="form-group">
                <label htmlFor="inputFile">Резюме</label>
                <input type="file" id="attachment" name='attachment'
                       onChange={this.changeFile} multiple />
                <p className="help-block">{this.state.error}</p>
            </div>
        )
    }
})

var ApplyForm = React.createClass({
    getInitialState: function() {
        return { errors: {}, sendWithErrors: false }
    },
    registerError: function(name, error) {
        this.state.errors[name] = error
        console.log(this.state.errors)
    },
    render: function() {
        return (
            <form className="form-horizontal" action=''>
                <input hidden value={this.props.securityToken} id="csrf_token" />
                <div className='form-group'>
                    <NameInput registerError={this.registerError} show={this.state.sendWithErrors} />
                    <EmailInput registerError={this.registerError} />
                    <PhoneInput registerError={this.registerError} />
                    <div className="form-group">
                        <textarea name='comment' id='comment' className="form-control"
                               placeholder="Коментарий" ></textarea>
                    </div>
                    <FileInput registerError={this.registerError} />
                    <input type='submit' />
                </div>
            </form>
        )
    }
})
var node = document.getElementById('attached-form');
var securityToken = node.dataset['securityToken'];
React.render(<ApplyForm securityToken={securityToken} />, node);
