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
    getList: function() {
        var filtered_data = this.props.data;
        if (this.props.category != 0) {
            filtered_data = filtered_data.filter(function(entry) {
                return (entry.category_id == this.props.category)
            }.bind(this));
        }
        if (this.props.city != 0) {
            filtered_data = filtered_data.filter(function(entry) {
                return (entry.city_id == this.props.city);
            }.bind(this));
        }
        return filtered_data;
    },
    render: function() {
        filtered_data = this.getList()
        var vaclist = filtered_data.map(function(p) {
            return <VacancyNode key={p.id} data={p} />
        });
        return (
            <div className="vacancyList"> {vaclist} </div>
        );
    }
});

var SpecSelect = React.createClass({
    handleChange: function(val) {
        this.props.onChange(this, val);
    },
    shouldComponentUpdate: function(nextProps, nextState) {
        return this.props.list !== nextProps.list;
    },
    render: function() {
        var options = [
            { value: '0', label: 'Все категории' },
        ];
        this.props.list.map(function(p) {
            options.push({ value: p.id, label: p.name })
        });
        return (
            <Select onChange={this.handleChange} clearable={false} options={options} placeholder="Категория" className="categoryDropdown">
            </Select>
        );
    }
});

var CitySelect = React.createClass({
    handleChange: function(val) {
        this.props.onChange(this, val);
    },
    shouldComponentUpdate: function(nextProps, nextState) {
        return this.props.list !== nextProps.list;
    },
    render: function() {
        var options = [
            { value: '0', label: 'Все города' },
        ];
        this.props.list.map(function(p) {
            options.push({ value: p.id, label: p.name })
        });
        return (
            <Select onChange={this.handleChange} clearable={false} options={options} placeholder="Город" className="cityDropdown">
            </Select>
        );
    }
});


var VacancyBox = React.createClass({
    getInitialState: function () {
        return {
            category: 0,
            city: 0,
            data: {categories: [], cities:[], vacancies:[],}
        };
    },
    handleSpecSelect: function(childComponent, val) {
        this.setState({
            category: parseInt(val)
        });
    },
    handleCitySelect: function(childComponent, val) {
        this.setState({
            city: parseInt(val)
        });
    },
    componentDidMount: function() {
        $.get(
            'list',
            function(result) {
                this.setState({
                    data: result
                });
            }.bind(this));
    },
    render: function() {
        return (
            <div className="vacancyBox">
            <SpecSelect onChange={this.handleSpecSelect} list={this.state.data.categories} ref="select" />
            <CitySelect onChange={this.handleCitySelect} list={this.state.data.cities} ref="select" />
            <VacancyList data={this.state.data.vacancies} category={this.state.category} city={this.state.city} ref="list"/>
            </div>
        );
    }
});

module.exports = VacancyBox;

