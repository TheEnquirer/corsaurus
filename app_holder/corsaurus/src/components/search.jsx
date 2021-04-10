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

    componentDidMount() 
    {
	this.setState({mounted: true})
	fetch('http://localhost:5000/query', {
	    method: 'put',
	    body: JSON.stringify(
		{
		    'num': 10,
		    'pos': ['king', 'woman'],
		    'neg': ['food'],
		    'mode': 'sum'
		}),
	    headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
	})
	    .then(res => res.json()).then((data) => 
		{
		    console.log(data, "data");
		    //this.setState({data: data});
		    this.props.set(data)
		})
		.catch((err) => console.error(err));
    }

    render()
    {
	return (
	    <div className="search-wrapper">
		yooooo
	    </div>
	)
    }
}

export default Search;

