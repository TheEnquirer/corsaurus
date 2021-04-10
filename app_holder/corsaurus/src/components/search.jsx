import './search.css';
import React, { Component } from 'react';
import autoBind from 'react-autobind';
//const autoBind = require('auto-bind/react');

class Search extends Component {
    constructor(props) 
    {
	super(props);
	autoBind(this);

	this.state = { mounted: false, data: [] };
    }

    parseString(v) {
	let pos = []
	let neg = []
	let lp = 0
	let rp = 0

	for (let i in v) {
	    if (v[i] != '+') {
		rp += 1;
	    } else {

	    }

	    if(v[i] != '-') {
		rp += 1;

	    } else {

	    }
	}
    }

    handleTextChange(e) {
    }

    handleSubmit(e) {
	if (e.key == "Enter") {
	    this.parseString(e.target.value)
	}
    }

    makeRequest(request) {
	fetch('http://localhost:5000/query', {
	    method: 'put',
	    body: JSON.stringify(request),
	    headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
	}).then(res => res.json()).then((data) => {
	    console.log(data, "data");
	    this.props.set(data)
	}).catch((err) => console.error(err));
    }

    componentDidMount() {
	this.setState({mounted: true})
	this.makeRequest(
	    {
		'num': 10,
		'pos': ['no'],
		'neg': [],
		'mode': 'sum'
	    }
	)
    }

    render() {
	return (
	    <div className="search-wrapper">
		<input className="search-input" 
		    onChange={this.handleTextChange}
		    onKeyDown={this.handleSubmit}
		    placeholder={"king + woman - man"}
		/>
	    </div>
	)
    }
}

export default Search;
