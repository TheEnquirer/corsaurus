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

