import './bars.css';
import { Spring, animated } from 'react-spring';
import React, { Component } from 'react';
import autoBind from 'react-autobind';
//const autoBind = require('auto-bind/react');

class VecViewer extends Component
{
    constructor(props)
    {
        super(props);
        autoBind(this);

        this.state = {
            data: [],
            mounted: false,
	    word: 'apple',
        };

    }

    queryWordvecs(request)
    {
        this.query(request)
            .then(data => {
                this.setState({data: data})
		console.log(data)
            });
    }

    async query(req) {
        return fetch('/query', { method: 'put', body: JSON.stringify(req) })
            .then(res => res.json())
            .then(data => {
                if (data.hasOwnProperty('error'))
                    throw data.error;
                else
                    return data.success;
            })
            .catch(console.error);
    }

    componentDidMount() {
	this.setState({mounted: true});
	this.queryWordvecs(
	    {
		'mode': 'get_vector',
		'word': this.state.word,
	    }
	);

    }

    render()
    {
        return (
            <div>
		yeeeet
            </div>
        )
    }
}

export default VecViewer;

