import './bars.css';
import { Spring, animated } from 'react-spring/renderprops';
import React, { Component } from 'react';
import autoBind from 'react-autobind';
//const autoBind = require('auto-bind/react');

class Bars extends Component {
    constructor(props) {
        super(props);
        autoBind(this);

        this.state = {
	    data: [["queen", 0.8407386541366577], ["monarch", 0.7541723847389221], ["prince", 0.7350203394889832], ["princess", 0.696908175945282], ["empress", 0.6771803498268127], ["sultan", 0.6649758815765381], ["Chakri", 0.6451102495193481], ["goddess", 0.6439394950866699], ["ruler", 0.6275452971458435], ["kings", 0.6273427605628967]],
	    mounted: false,
	}
    }

    processData() {
	let processed = this.state.data.map((item, i) => {
	    return [item[0].replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); }), item[1]]
	})
	this.setState({data: processed})
	console.log(processed)
    };

    componentDidMount() {
	this.setState({mounted: true})
	this.processData()
    }

    render() {
	return (
	    <div className="bars-wrapper">
		{this.state.mounted? this.state.data.map((item, i) =>  (
		    <div className="bar-unit">
			<div className="word-wrapper">
			    <div className="word">{item[0]}</div>
			</div>
			<Spring native to={{width: item[1] * 500}}>
			    {props =>
				<animated.div className="bar-gradient" style={{...props}}>&nbsp;</animated.div>
			    }
			</Spring>

		    </div>
		)) : ""}

	    </div>
        )
    }
}

export default Bars;
