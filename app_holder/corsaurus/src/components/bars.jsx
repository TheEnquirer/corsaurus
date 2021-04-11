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
		shown: 1,
	    };

	    this.more = React.createRef();
	}

    wid = -1

    processData() {
        let widest = -1
        let processed = this.props.data.map((item, i) => {
            widest = Math.max(widest, item[0].length)
            return [item[0].replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); }), item[1]]
        });
        //this.setState({data: processed, wid: widest});
        this.setState({data: processed});
        this.wid = widest*12
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

    render() {
	return (
	    <div className="bars-wrapper">
		{(this.state.mounted && this.state.data)? this.state.data.slice(0, 10*this.state.shown).map((item, i) => (
		    <div className="bar-unit" style={{width: this.wid+620}}>
			<div className="word-wrapper" style={{width: this.wid}}>
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
		)) : "nothing returned :("}
		<div
		    ref={this.more}
		>
		    <p 
		    className="arrow"
		    onClick={() => {
			console.log(this.state.shown*10, this.state.data.length)
			if (this.state.shown*10 <= this.state.data.length) { 
			    this.setState({shown: this.state.shown + 1}, () => {
				if (this.more) {
				    this.more.current.scrollIntoView({
					behavior: "smooth", 
					block: "start",
				    })
				    console.log("scrolling")
				}
			    })
			}
		    }}
		>{(this.state.shown*10 <= this.state.data.length)? "▼" : "∅"} </p>
		</div>

	    </div>
	)
    }
}

export default Bars;
