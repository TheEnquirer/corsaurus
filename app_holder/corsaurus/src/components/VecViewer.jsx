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
	    word: 'man',
	    words: [
		//'man', 'woman', 'boy', 'girl', 'apple', 'orange', 'pear', 'avocado', 'tomato'
		//'i', 'love', 'you',
		//'mean', 'rude', 'horrible', 'nice', 'amazing'
		'Acai', 'Apples', 'Apricots', 'Avocado', 'Ackee', 'Bananas', 'Bilberries', 'Blueberries', 'Blackberries', 'Boysenberries', 'Bread', 'fruit', 'Cantaloupes', '(cantalope)', 'Chocolate-Fruit', 'Cherimoya', 'Cherries', 'Cranberries', 'Cucumbers', 'Currants', 'Dates', 'Durian', 'Eggplant', 
		//'Elderberries', 'Figs', 'Gooseberries', 'Grapes', 'Grapefruit', 'Guava', 'Honeydew', 'melons', 'Horned', 'melon', '(Kiwano)', 'Huckleberries', 'Ita', 'Palm', 'Jujubes', 'Kiwis', 'Durian.jpg', 'Kumquat', 'Lemons', 'Limes', 'Lychees', 'Mangos', 'Mangosteen', 'Mulberries', 'Muskmelon', 'Nectarines', 'Ogden', 'melons', 'Olives', 'Oranges', 'Papaya', 'Passion', 'fruit', 'Peaches', 'Pears', 'Peppers', 'Persimmon', 'Pineapple', 'Plums'
	    ]
	};

    }

    queryWordvecs(request)
    {
	let d = this.query(request)
	    .then(v => {
		this.setState({data: [...this.state.data, v]})
	    });
	return d
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
	//console.log(`rgb(${rgb.join()+")"}`)
	return rgb;
    }

    componentDidMount() {
	document.body.style = 'background: #202020;';
	this.setState({mounted: true});
	this.state.words.map( async (w) => {
	    const d = await this.queryWordvecs(
		{
		    'mode': 'get_vector',
		    'word': w,
		}
	    )
	    return d
	})
	//console.log(this.state.data)
    }

    render()
    {
        return (
	    <div className="big-wrapper">
		{this.state.words.map((word, i) => {
		    return (
			<div className="r-wrapper">
			    {this.state.data[i]? <p className="vword"> {word} </p> : ""}
			    {this.state.data[i]? this.state.data[i].map((v) => {
				return (
				    <div>
					<div
					    style={{
						backgroundColor: `rgb(${this.pickHex([169, 49, 49], [65, 105, 225], v*0.2).join()+")"}`
						//backgroundColor: `rgb(0, 225, 0)`
					    }}
					    className="r"></div>
				    </div>
				)
			    }) : ""} </div>

		    )
		})}
	    </div>
	)
    }
}

export default VecViewer;

