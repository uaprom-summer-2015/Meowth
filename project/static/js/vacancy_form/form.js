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
    render: function() {
        return (
            <form>
                <label>Имя:<br/>
                    <input value={this.state.name}
                           onChange={this.handleChangeName}
                           type='text'
                           className={this.valid(this.validateName())} />
                </label><br/>
                <label>Email:<br/>
                    <input value={this.state.email}
                           onChange={this.handleChangeEmail}
                           type='text'
                           className={this.valid(this.validateEmail())}/>
                </label><br/>
                <label>Телефон:<br/>
                    <input value={this.state.phone}
                           onChange={this.handleChangePhone}
                           type='text'
                           className={this.valid(this.validatePhone())} />
                </label><br/>
                <label>Коментарий:<br/>
                    <input type='text'/>
                </label><br/>
                <label>Резюме:<br/>
                    <input type='file' />
                </label><br/>
                <input type='submit' />
            </form>
        )
    }
})

React.render(<ApplyForm />, document.getElementById('attached-form'))