import './bars.css';
import './VecViewer.css';
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

    pickHex(color1, color2, weight) {
	var w1 = weight;
	var w2 = 1 - w1;
	var rgb = [Math.round(color1[0] * w1 + color2[0] * w2),
	    Math.round(color1[1] * w1 + color2[1] * w2),
	    Math.round(color1[2] * w1 + color2[2] * w2)];
	console.log(`rgb(${rgb.join()+")"}`)
	return rgb;
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
		<div className="r-wrapper">
		    <p className="vword"> {this.state.word} </p>
		    {this.state.data.map((v) => {
			return (
			    <div>
				<div
				    style={{
					backgroundColor: `rgb(${this.pickHex([255,0,0], [0,128,0], v).join()+")"}`
					//backgroundColor: `rgb(0, 225, 0)`
				    }}
				className="r"></div>
			    </div>
			)
		    })} </div>
	    </div>
	)
    }
}

export default VecViewer;

