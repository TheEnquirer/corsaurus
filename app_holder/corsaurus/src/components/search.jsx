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

    parseString() {

    }

<<<<<<< HEAD
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

    componentDidMount() 
    {
	this.setState({mounted: true})
	this.makeRequest(
	    {
		'num': 10,
		'pos': ['king', 'woman'],
		'neg': ['man'],
		'mode': 'sum'
	    }
	)
    }

    render()
    {
	return (
	    <div className="search-wrapper">
		yooooo
	    </div>
	)
=======
		// fetch('http://localhost:5000/test', {
		// 	method: 'PUT',
		// 	body: JSON.stringify(
		// 	{
		// 		'test': 'yes.'
		// 	}),
		// 	headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
		// })
		// 	.then(res => res.json()).then(data => {
		// 		console.log(data);
		// 	})
		// 	.catch(err => console.error(err));
		fetch('http://localhost:5000/query', {
			method: 'put',
			body: JSON.stringify(
			{
			  'num': 10,
			  'pos': ['king', 'woman'],
			  'neg': ['man'],
			  'mode': 'sum'
			}),
			headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
		  })
		  	.then(res => res.json()).then((data) => 
			{
				console.log(data);
				this.setState({data: data});
			})
			.catch((err) => console.error(err));
    }

    render() 
	{
		return (
	    	<div className="search-wrapper">
			From the backend:
			<br></br>
			{this.state.data}
	    	</div>
        )
>>>>>>> 933c9da5b7ca7ecf8aefe6cb0f32af6d0c6be8c7
    }
}

export default Search;

