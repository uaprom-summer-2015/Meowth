var ExpandButton = React.createClass({
    handleClick: function(e) {
        this.props.click(e);
    },
    render: function() {
        return (<img src="../static/media/jacob.jpg" onClick={this.handleClick} className="vacancyButton"></img>);
    }
});

var VacancyNodeCompressed = React.createClass({
    getInitialState: function() {
        return {
            data: []
        };
    },
    componentDidMount: function() {
        this.setState({
            data: this.props.data
        });
    },
    handleButtonClick: function(e) {
        this.props.click(e);
    },
    render: function() {
        return (
            <div className="vacancyNodeCompressed">
            <ExpandButton ref="button" click={this.handleButtonClick} />
            <p className="vacancyTitle">{this.state.data.title}</p>
            </div>
        );
    }
});


var VacancyNodeExpanded = React.createClass({
    getInitialState: function() {
        return {
            data: []
        };
    },
    componentDidMount: function() {
        this.setState({
            data: this.props.data
        });
    },
    handleButtonClick: function(e) {
        this.props.click(e);
    },
    render: function() {
        return (
            <div className="vacancyNodeExpanded">
            <ExpandButton ref="button" click={this.handleButtonClick} />
            <p className="vacancyTitle">{this.state.data.title}</p>
            <p className="vacancyDescr">{this.state.data.short_description}</p>
            </div>
        );
    }
});

var VacancyNode = React.createClass({
    getInitialState: function() {
        return {
            data: [],
            expanded: false
        };
    },
    componentDidMount: function() {
        this.setState({
            data: this.props.data
        });
    },
    handleButtonClick: function(e) {
        this.setState({
            expanded: !this.state.expanded
        });
    },
    render: function() {
        if (!this.state.expanded) {
            return (<VacancyNodeCompressed data={this.props.data} click={this.handleButtonClick} />);
        } else {
            return (<VacancyNodeExpanded data={this.props.data} click={this.handleButtonClick} />);
        }
    }
});

var VacancyList = React.createClass({
    getInitialState: function() {
        return {
            data: [],
            category: 0
        };
    },
    getList: function(value) {
        $.get('list?category_id='+value.toString(), function(result) {
            this.setState({
                data: result.vacancies
            });
        }.bind(this));
    },
    componentDidMount: function() {
        this.getList('0');
    },
    render: function() {
        var vaclist = this.state.data.map(function(p) {
            return <VacancyNode key={p.id} data={p} />
        });
        return (
            <div className="vacancyList"> {vaclist} </div>
        );
    }
});

var SpecSelect = React.createClass({
    getInitialState: function() {
        return {
            choices: [],
            value: 0
        };
    },
    getList: function() {
        $.get('list?category_id=0', function(result) {
            this.setState({
                choices: result.categories
            });
        }.bind(this));
    },
    componentDidMount: function() {
        this.getList();
    },
    handleChange: function(e) {
        this.props.onChange(this, e);
    },
    render: function() {
        var catlist = this.state.choices.map(function(p) {
            return <option value={p.id}>{p.name}</option>
        });
        var blank = <option value="0">Любой</option>
        return (
            <select onChange={this.handleChange} value={this.state.value} className="categoryDropdown"> {blank} {catlist} </select>
        );
    }
});

var VacancyBox = React.createClass({
    handleSelect: function(childComponent, e) {
        childComponent.setState({
            value: e.target.value
        });
        this.refs.list.getList(e.target.value);
    },
    render: function() {
        return (
            <div className="vacancyBox">
            <SpecSelect onChange={this.handleSelect} ref="select" />
            <VacancyList ref="list"/>
            </div>
        );
    }
});


React.render(
    <VacancyBox />,
    document.body
);