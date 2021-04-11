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
	let p = "+"

	this.pusher = (i) => {
	    let mod = v.slice(lp, i).replace(/((?<!\\)[+-\\])+/, "").trim()
	    if (p == '+') { pos.push(mod) } else { neg.push(mod) }
	}

	for (let i in v) {
	    if ((v[i-1] != "\\") && ((v[i] == '-') || (v[i] == '+'))) {
		if (i != lp) {
		    this.pusher(i)
		    lp = i
		}
		p = v[i]
	    }
	    if (i == v.length - 1) { this.pusher(i+1) }
	}
	console.log(pos, neg, "whee")
	return [pos, neg]
    }

    checkText(v) {

    }

    handleTextChange(e) {
    }

    handleSubmit(e) {
	if (e.key == "Enter") {
	    let parsed = this.parseString(e.target.value)
	    this.makeRequest( 
		{
		    'num': 10,
		    'pos': parsed[0],
		    'neg': parsed[1],
		    'mode': 'sum'
		}
	    )
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
