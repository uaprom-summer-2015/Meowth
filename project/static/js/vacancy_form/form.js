var ApplyForm = React.createClass({
    getInitialState: function() {
    return {name: '', email: '', phone: ''}
    },
    handleChangeName: function(e) {
        this.setState({
            name: e.target.value
        })
    },
    handleChangeEmail: function(e) {
        this.setState({
            email: e.target.value
        })
    },
    handleChangePhone: function(e) {
        this.setState({
            phone: e.target.value
        })
    },
    handleChangeFile: function(e) {
        this.validateSize(e.target.files[0].size)
    },
    validateName: function() {
        return this.state.name != ''
    },
    validateEmail: function() {
        return /.+@.+\..+/.test(this.state.email)
    },
    validatePhone: function() {
        return /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/.test(this.state.phone)
    },
    valid: function(bool) {
        return bool ? 'valid' : 'invalid'
    },
    validateSize: function(size) {
        if (size > 15 * 1024 * 1024) {
            alert('To big file for uploading (15Mb - max)');
        }
    },
    render: function() {
        return (
            <div>
                <label>Имя:<br/>
                    <input name='name' id='name'
                           value={this.state.name}
                           onChange={this.handleChangeName}
                           type='text'
                           className={this.valid(this.validateName())} />
                </label><br/>
                <label>Email:<br/>
                    <input name='email' id='email'
                           value={this.state.email}
                           onChange={this.handleChangeEmail}
                           type='text'
                           className={this.valid(this.validateEmail())}/>
                </label><br/>
                <label>Телефон:<br/>
                    <input name='phone' id='phone'
                           value={this.state.phone}
                           onChange={this.handleChangePhone}
                           type='text'
                           className={this.valid(this.validatePhone())} />
                </label><br/>
                <label>Коментарий:<br/>
                    <input name='comment' id='comment'
                           type='text'/>
                </label><br/>
                <label>Резюме:<br/>
                    <input name='files[]' id='attachment'
                           type='file'
                           onChange={this.handleChangeFile} multiple />
                </label><br/>
                <input type='submit' />
            </div>
        )
    }
})

React.render(<ApplyForm />, document.getElementById('attached-form'))
