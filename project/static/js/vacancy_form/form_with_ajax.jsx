var ApplyForm = React.createClass({
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
        var nameClass = "form-horizontal" + (this.state.nameError ? ' has-error' : '');
        var emailClass = "form-horizontal" + (this.state.emailError ? ' has-error' : '');
        var phoneClass = "form-horizontal" + (this.state.phoneError ? ' has-error' : '');
        if (this.state.success == false) {
            return (
                <form className="form-horizontal" action='form' name='ApplyForm' id='ApplyForm'
                      onSubmit={this.handleSubmit} encType="multipart/form-data" ref='ApplyForm'>

                    <input type='hidden' name="csrf_token" value={this.props.csrf_token} />

                    <div className={nameClass} >
                        <label className="control-label" htmlFor="name">{ this.state.nameError }</label>
                        <input name='name' type="text" className="form-control" id="name"
                               placeholder="Имя" value={this.state.name} onChange={this.changeName} />
                    </div>

                    <div className={emailClass} >
                        <label className="control-label" htmlFor="email">{ this.state.emailError }</label>
                        <input name='email' type="email" className="form-control" id="email"
                               placeholder="Email" value={this.state.email} onChange={this.changeEmail} />
                    </div>

                    <div className={phoneClass} >
                        <label className="control-label" htmlFor="phone">{ this.state.phoneError }</label>
                        <input name='phone' type="text" className="form-control" id="phone"
                               placeholder="Телефон" value={this.state.phone} onChange={this.changePhone} />
                    </div>

                    <div className="form-group">
                        <textarea name='comment' id='comment' className="form-control"
                                  placeholder="Коментарий" ></textarea>
                    </div>

                    <div className="form-group">
                        <label htmlFor="inputFile">Резюме</label>
                        <input type="file" id="attachment" name='attachment'
                               onChange={this.changeFile} multiple />
                        <div className='has-error'>
                            <p className="help-block">{this.state.fileError}</p>
                        </div>
                    </div>

                    <input type='submit' />
                </form>
            );
        } else {
            return (
                <h2>Success</h2>
            );
        }
    }
})

var node = document.getElementById('attached-form');
var csrf_token = document.getElementById('csrf_token').content;
React.render(<ApplyForm csrf_token={csrf_token} />, node);
