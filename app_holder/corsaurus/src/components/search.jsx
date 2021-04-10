import './search.css';
import React, { Component } from 'react';
import autoBind from 'react-autobind';
//const autoBind = require('auto-bind/react');

class Search extends Component 
{
    constructor(props) 
	{
        super(props);
        autoBind(this);

        this.state = { mounted: false, data: [] };
    }

    componentDidMount() 
	{
		this.setState({mounted: true})
		// fetch('http://localhost:5000/query', { 
		// method: 'PUT', 
		// body: JSON.stringify(
		// 	{
		// 		'num': 10,
		// 		'pos': ['king', 'woman'],
		// 		'neg': ['man']
		// 	}),
		// headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
		// })
		// .then(res =>
		// {
		// 	console.log(res, "ghee")
		// 	let val = JSON.parse(res.text());
		// 	console.log(val)
		// })
		// .catch(err => err)

		// fetch('/test').then(data => {
		// console.log(data)
		// });
		// fetch('/time').then(data => {
		// console.log(data);
		// });

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
    }
}

export default Search;

