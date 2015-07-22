var React = require('react'),
    navigate = require('react-mini-router').navigate,
    Select = require('react-select');

var $ = require('jquery');

$.QueryString = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'))


function range(start, stop, step) {
    if (typeof stop == 'undefined') {
        // one param defined
        stop = start;
        start = 0;
    }

    if (typeof step == 'undefined') {
        step = 1;
    }

    if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
        return [];
    }

    var result = [];
    for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
        result.push(i);
    }

    return result;
};

if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

var Paginate = React.createClass({
    handleClick: function(e) {
        this.props.click(e, e.target.id);
    },
    render: function() {
        var page = this.props.page;
        var pageAmount = this.props.pagesAmount;
        result = range(pageAmount).map(function(p, key) {
            if (p == page) {
                return <div className="page selected" key={key}><span id={key}>{p+1}</span></div>
            } else {
                return <div className="page" onClick={this.handleClick} key={key} id={key}><span id={key}>{p+1}</span></div>
            }
        }.bind(this));
        return (<div className="paginator"> {result} </div>)
    }
});

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
        city_id = this.state.data.city_id
        citylist = this.props.citylist
        city = citylist.filter(function(n) {
            return n.id == city_id;
        }).map(function(n) {
            return n.name;
        });
        return (
            <div className="panel panel-default vacancyNodeCompressed">
            <ExpandButton expanded={this.props.expanded} ref="button" click={this.handleButtonClick} />
            <p className="vacancyTitle"> <a href={this.state.data.name_in_url}>{this.state.data.title}</a></p>
            <p className="vacancyCity">{city}</p> <p className="vacancySalary">{this.state.data.salary}</p>
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
    handleToVacancyClick: function() {
        window.location.href = this.state.data.name_in_url;
    },
    render: function() {
        city_id = this.state.data.city_id
        citylist = this.props.citylist
        city = citylist.filter(function(n) {
            return n.id == city_id;
        }).map(function(n) {
            return n.name;
        });
        return (
            <div className="panel panel-default vacancyNodeExpanded">
            <ExpandButton expanded={this.props.expanded} ref="button" click={this.handleButtonClick} />
            <p className="vacancyTitle"> <a href={this.state.data.name_in_url}>{this.state.data.title}</a></p>
            <p className="vacancyCity">{city}</p> <p className="vacancySalary">{this.state.data.salary}</p>
            <p className="vacancyDescr">{this.state.data.short_description}</p>
            <button type="button" onClick={this.handleToVacancyClick} className="btn btn-info goToVacancyButton">Перейти к вакансии</button>
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
            return (<VacancyNodeCompressed citylist={this.props.citylist} expanded={this.state.expanded} ref="node" className="col-xs-6 col-sm-4" data={this.props.data} click={this.handleButtonClick} />);
        } else {
            return (<VacancyNodeExpanded citylist={this.props.citylist} expanded={this.state.expanded} ref="node" className="col-xs-6 col-sm-4" data={this.props.data} click={this.handleButtonClick} />);
        }
    }
});

var VacancyList = React.createClass({
    getInitialState: function () {
        qs = $.QueryString;
        var page = '1';
        if ('page' in qs) {
            page = $.QueryString['page'];
        }
        return {
            page: parseInt(page)-1
        };
    },
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
    handlePageClick: function(e, val) {
        this.setState({page: parseInt(val)});
        navigate('?city={0}&category={1}&page={2}'.format(this.props.parent.state.city, this.props.parent.state.category, parseInt(val)+1), true);
    },

    render: function() {
        per_page = this.props.per_page
        page = this.state.page
        filtered_data = this.getList()
        amount = Math.ceil(filtered_data.length / per_page);
        if (page>amount-1) {
            page=amount-1;
        }
        if (page<0) {
            page=0;
        }
        offset = per_page*page;
        filtered_data = this.getList().slice(offset, offset+per_page)
        var vaclist = filtered_data.map(function(p) {
            return <VacancyNode key={p.id} citylist={this.props.citylist} data={p} />
        }.bind(this));
        return (
            <div className="vacancyList">
            {vaclist}
            <Paginate pagesAmount={amount} page={page} click={this.handlePageClick} ref="paginate"/>
            </div>
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

        initial_value = options.filter(function(n) {
            return n.value == this.props.value;
        }.bind(this)).map(function(n) {
            return n.label;
        })[0];

        if (this.props.value == 0) {
            initial_value = '';
        }
        return (
            <Select onChange={this.handleChange} clearable={false} value={initial_value} options={options} placeholder="Категория" className="categoryDropdown">
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

        initial_value = options.filter(function(n) {
            return n.value == this.props.value;
        }.bind(this)).map(function(n) {
            return n.label;
        })[0];

        if (this.props.value == 0) {
            initial_value = '';
        }

        return (
            <Select onChange={this.handleChange} clearable={false} value={initial_value} options={options} placeholder="Город" className="cityDropdown">
            </Select>
        );
    }
});


var VacancyBox = React.createClass({
    getInitialState: function () {
        return {
            category: 0,
            city: 0,
            data: {categories: [], cities:[], vacancies:[],},
        };
    },
    handleSpecSelect: function(childComponent, val) {
        this.setState({
            category: parseInt(val)
        });
        navigate('?city={0}&category={1}&page={2}'.format(this.state.city, val, this.refs.list.state.page), true);
    },
    handleCitySelect: function(childComponent, val) {
        this.setState({
            city: parseInt(val)
        });
        navigate('?city={0}&category={1}&page={2}'.format(val, this.state.category, this.refs.list.state.page), true);
    },
    componentDidMount: function() {
        qs = $.QueryString;
        var city_id = '0';
        var category_id = '0';
        if ('city' in qs) {
            city_id = $.QueryString['city'];
        }
        if ('category' in qs) {
            category_id = $.QueryString['category'];
        }
        $.get(
            'list',
            function(result) {
                this.setState({
                    data: result,
                    city: parseInt(city_id),
                    category: parseInt(category_id),
                });
            }.bind(this));

    },
    render: function() {
        results = this.state.data.vacancies;
        offset = 2*this.state.page;
        amount = Math.ceil(results.length / 2);
        return (
            <div className="vacancyBox">
            <SpecSelect onChange={this.handleSpecSelect} value={this.state.category} list={this.state.data.categories} ref="select" />
            <CitySelect onChange={this.handleCitySelect}  value={this.state.city} list={this.state.data.cities} ref="select" />
            <VacancyList per_page={5} data={results} parent={this} citylist={this.state.data.cities} category={this.state.category} city={this.state.city} ref="list"/>
            </div>
        );
    }
});

module.exports = VacancyBox;

