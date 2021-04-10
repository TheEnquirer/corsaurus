import './bars.css';
import { Spring, animated } from 'react-spring';
import React, { Component } from 'react';
import autoBind from 'react-autobind';
//const autoBind = require('auto-bind/react');

class Bars extends Component 
{
    constructor(props) 
	{
        super(props);
        autoBind(this);

        this.state = {
	    data: this.props.data,
	    mounted: false,
	};
    }

    processData() {
	let processed = this.props.data.map((item, i) => {
	    return [item[0].replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); }), item[1]]
	});
	this.setState({data: processed});
    };

    componentDidMount() {
	this.setState({mounted: true});
	this.processData();
    }

    componentDidUpdate(prevProps, prevState) {
	if (this.props !== prevProps) {
	    this.processData()
	}
    }

    render() 
	{
		return (
			<div className="bars-wrapper">
				    {console.log(this.state.data, "here")}
			{this.state.mounted? this.state.data.map((item, i) => (
				<div className="bar-unit">
				<div className="word-wrapper">
					<div className="word">{item[0]}</div>
				</div>
				<Spring native to={{width: 500}}>
					{props =>
					<animated.div className="bottom-gradient" style={{...props}}>&nbsp;</animated.div>
					}
				</Spring>
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
