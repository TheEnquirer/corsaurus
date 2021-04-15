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

    parseString(v, innerHTMLSetter=null) 
    {
	let pos = [];
	let neg = [];
	let lp = 0;
	let p = "+";
    let full = [];
    let tok_info = [];

	this.pusher = (i) => {
	    let mod = v.slice(lp, i).replace(/((?<!\\)[+-\\])+/, "").trim();
		// eslint-disable-next-line
	    if (p == '+') { pos.push(mod) } else { neg.push(mod) }
        full.push(mod);
        tok_info.push([p == '+' ? 'pos' : 'neg', lp, i]);
	}

	for (let i in v) 
	{
		// eslint-disable-next-line
	    if ((v[i-1] != "\\") && ((v[i] == '-') || (v[i] == '+'))) 
	    {
		// eslint-disable-next-line
		if (i != lp) // NOTE: exr0n doesn't understand why we need this if statement
		{
		    this.pusher(i);
		    lp = i;
		}
		p = v[i];
	    }
		// eslint-disable-next-line
	    if (i == v.length - 1) { this.pusher(i+1) }
	}

	//let full = [...pos, ...neg]
    console.log(full)
	if (full.length == 0) { return [0, ""] }
    let bad = false;    
	for (let i in full) {
        const [ color, lhs, rhs ] = tok_info[i];
	    if (full[i].includes(" ")) {
            bad = true;
            full[i] = `<span class="syntaxhlerr">${v.slice(lhs, rhs)}</span>`
	    } else {
            full[i] = `<span class="syntaxhl${color}">${v.slice(lhs, rhs)}</span>`
        }
	}
    console.log(full)
    console.log('\n')
    if (typeof innerHTMLSetter === 'function') innerHTMLSetter(full.join(""));

    if (bad) return [0, "Please seperate words with either + or -"];
	return [1, [pos, neg]]
    }

    clenseInputPaste(e) {
        setTimeout(() => {

            // set caret to the end of the range
            // https://stackoverflow.com/a/52085710/10372825
            let range = document.createRange();
            range.selectNodeContents(e.target);
            range.collapse(false);
            let selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
        }, 0);
    }
    cleanseInputNewlines(e) {
        // https://stackoverflow.com/a/33239883/10372825
        if (e.keyCode === 13) {
            this.handleSubmit(e);
            e.preventDefault();
        }
    }
    
    handleTextChange(e) {
	this.setState({inputval: e.target.value.toLowerCase()})
    }

    actuallyHandleTextChange(e) {
        setTimeout(() => {
            // clense content of html
            // https://stackoverflow.com/a/47140708/10372825
            let val = new DOMParser().parseFromString(e.target.innerHTML, 'text/html');
            
            e.target.innerHTML = (val.body.textContent || "").replace(/\n/g, ' ');
            this.setState({inputval: e.target.innerHTML.toLowerCase()})
            this.parseString(e.target.innerHTML, (v) => { e.target.innerHTML = v });
        }, 0);
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
			this.props.setShown(1)
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
		<div className="search-input" 
		    onChange={this.handleTextChange /* UM HUX @TheEnquirer THIS NEVER GETS CALLED */ } 
		    onInput={this.actuallyHandleTextChange}
		    onKeyDown={this.handleSubmit}
		    placeholder={"king + woman - man"}
            contentEditable={true}
            onKeyDown={this.cleanseInputNewlines}
            onPaste={this.clenseInputPaste}
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
