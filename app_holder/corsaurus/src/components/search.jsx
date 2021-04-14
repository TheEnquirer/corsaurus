import './search.css';
import React, { Component } from 'react';
import autoBind from 'react-autobind';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';

//const autoBind = require('auto-bind/react');

class Search extends Component 
{
    constructor(props) 
    {
	super(props);
	autoBind(this);

	this.state = { 
	    mounted: false, 
	    data: [],
	    errormsg: "",
	    inputval: "",
	    prevSearch: "",
	};
    }

    parseString(v) 
    {
	let pos = [];
	let neg = [];
	let lp = 0;
	let p = "+";

	this.pusher = (i) => {
	    let mod = v.slice(lp, i).replace(/((?<!\\)[+-\\])+/, "").trim();
		// eslint-disable-next-line
	    if (p == '+') { pos.push(mod) } else { neg.push(mod) }
	}

	for (let i in v) 
	{
		// eslint-disable-next-line
	    if ((v[i-1] != "\\") && ((v[i] == '-') || (v[i] == '+'))) 
	    {
		// eslint-disable-next-line
		if (i != lp) 
		{
		    this.pusher(i);
		    lp = i;
		}
		p = v[i];
	    }
		// eslint-disable-next-line
	    if (i == v.length - 1) { this.pusher(i+1) }
	}

	let full = [...pos, ...neg]
	if (full.length == 0) { return [0, ""] }
	for (let i in full) {
	    if (full[i].includes(" ")) {
		return [0, "Please seperate words with either + or -"]
	    }
	}

	return [1, [pos, neg]]
    }


    handleTextChange(e) {
	this.setState({inputval: e.target.value})
    }

    handleSubmit(e) {
	if (((e.key === "Enter") || (e.type == "click")) && this.state.inputval != this.state.prevSearch) {
	    this.setState({prevSearch: this.state.inputval})
	    let parsed = this.parseString(this.state.inputval);
	    if (parsed[0] == 1) {
		this.makeRequest( 
		    {
			'num': 100,
			'pos': parsed[1][0],
			'neg': parsed[1][1],
			'mode': 'sum'
		    }
		);
	    } else {
		this.setState({errormsg: parsed[1]})
	    }
	}
    }

    makeRequest(request) 
    {
	fetch('/query', 
	    {
		method: 'put',
		body: JSON.stringify(request),
		headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
	    })
	    .then(res => res.json()).then((data) => 
		{
		    if (data.hasOwnProperty('error')) {
			if (data.error == "out_of_vocab") {
			    this.setState({errormsg: "We don't recognize a word.."})
			}
			throw data.error;
		    } else {
			this.setState({errormsg: ""})
			this.props.set(data.success)
		    }
		})
		.catch(console.error);
    }

    componentDidMount() {
	this.setState({mounted: true})
	this.makeRequest(
	    {
		'num': 100,
		'pos': ['king', 'woman'],
		'neg': ['man'],
		'mode': 'sum'
	    }
	)
    }

    render() {
	return (
	    <div className="search-wrapper">
		<FontAwesomeIcon icon={faSearch} onClick={this.handleSubmit} className="icon"/>
		<input className="search-input" 
		    onChange={this.handleTextChange}
		    onKeyDown={this.handleSubmit}
		    placeholder={"king + woman - man"}
		/>
		{(this.state.errormsg != "")?
		    <div className="errormsg"> 
		     <FontAwesomeIcon icon={faExclamationTriangle} className="error-icon"/>
		    {this.state.errormsg} 
		    </div>
		    : ""}
	    </div>
	)
    }
}

export default Search;
