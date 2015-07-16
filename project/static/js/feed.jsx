var React = require('react');
var $ = require('jquery');
var Select = require('react-select');

var ExpandButton = React.createClass({
    handleClick: function(e) {
        this.props.click(e);
    },
    render: function() {
        return (<button type="button" onClick={this.handleClick} className="vacancyButton btn btn-info btn-circle" aria-label="Left Align">
                 <span className={this.props.expanded ? "glyphicon glyphicon-menu-up" : "glyphicon glyphicon-menu-down"}>
                 </span>
                </button>);
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
            <div className="panel panel-default">
            <ExpandButton expanded={this.props.expanded} ref="button" click={this.handleButtonClick} />
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
            <div className="panel panel-default">
            <ExpandButton expanded={this.props.expanded} ref="button" click={this.handleButtonClick} />
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
            return (<VacancyNodeCompressed expanded={this.state.expanded} ref="node" className="col-xs-6 col-sm-4" data={this.props.data} click={this.handleButtonClick} />);
        } else {
            return (<VacancyNodeExpanded expanded={this.state.expanded} ref="node" className="col-xs-6 col-sm-4" data={this.props.data} click={this.handleButtonClick} />);
        }
    }
});

var VacancyList = React.createClass({
    getInitialState: function() {
        return {
            data: [],
            dataToRender: [],
            category: 0,
            city: 0
        };
    },
    getList: function() {
        $.get(
            'list',
            function(result) {
                this.setState({
                    data: result.vacancies,
                    dataToRender: result.vacancies
                });
            }.bind(this));
    },
    calcList: function() {
        var city = this.state.city;
        var category = this.state.category;
        var newdata = this.state.data.filter(function(i,n) {
                return n.category_id==category;
            });
        this.setState({dataToRender: newdata});
    },
    componentDidMount: function() {
        this.getList();
    },

    render: function() {
        var vaclist = this.state.dataToRender.map(function(p) {
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
        };
    },
    getList: function() {
        $.getJSON(
            'list',
            function(result) {
                    this.setState({
                        choices: result.categories
                    });
            }.bind(this));
    },

    componentDidMount: function() {
        this.getList();
    },

    handleChange: function(val) {
        this.props.onChange(this, val);
    },

    render: function() {
        var options = [
            { value: '0', label: 'Все категории' },
        ];
        this.state.choices.map(function(p) {
            options.push({ value: p.id, label: p.name })
        });
        return (
            <Select onChange={this.handleChange} clearable={false} options={options} placeholder="Категория" className="categoryDropdown">
            </Select>
        );
    }
});

var VacancyBox = React.createClass({
    handleSelect: function(childComponent, val) {
        this.refs.list.setState({category: parseInt(val)});
        this.refs.list.calcList();
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

module.exports = VacancyBox;

