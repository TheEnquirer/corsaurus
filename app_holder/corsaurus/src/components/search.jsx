import './search.css';
import React, { Component } from 'react';
import autoBind from 'react-autobind';
//const autoBind = require('auto-bind/react');

class Search extends Component {
    constructor(props) {
        super(props);
        autoBind(this);

        this.state = {
	    mounted: false,
	}
    }


    componentDidMount() {
	this.setState({mounted: true})
	//fetch('http://localhost:5000/query', { 
	//    method: 'PUT', 
	//    body: JSON.stringify(
	//        {
	//            'num': 10,
	//            'pos': ['king', 'woman'],
	//            'neg': ['man']
	//        }),
	//    headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
	//})
	//.then(res =>
	//    {
	//        console.log(res, "ghee")
	//        let val = JSON.parse(res.text());
	//        console.log(val)
	//    })
	//    .catch(err => err)

	//fetch('/test').then(data => {
	//    console.log(data)
	//});
	//fetch('/time').then(data => {
	//  console.log(data);
	//});

	fetch('http://localhost:5000/time',
	    {
		method: 'PUT',
		body: JSON.stringify(
		    {
			'test': 'yes.'
		    }),
		headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
	    }
	).then(res => res.json()).then(data => {
	    console.log(data);
	});
    }

    render() {
	return (
	    <div className="search-wrapper">
		yooooo

	    </div>
        )
    }
}

export default Search;

