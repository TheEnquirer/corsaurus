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
            //shown: 1,
            loading: true,
            hovering: -1,
            copied: -1,
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
	this.setState({data: processed, hovering: -1, copied: -1});
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
        if (this.state.data.length !== 0 && this.state.loading) { this.setState({ loading: false }); }
    }

    moreIndicator() 
    {
        if (this.state.data.length === 0) { return ""; }
        else
        {
            if (this.props.shown*10 <= this.state.data.length) { return "▼"; }
            else { return "∅"; }
        }
    }

    loadingIndicator() 
    {
        return this.state.loading && (
            <div className="loader"></div>
        );
    }

    render() 
    {
        return (
            <div>
                <div className="bars-wrapper">
                    {(this.state.mounted && this.state.data)? this.state.data.slice(0, 10*this.props.shown).map((item, i) => (
                        <div className="bar-unit" style={{width: this.wid+620}} key={item[0]+i}>
                            <div 
				className="word-wrapper" 
				style={{width: this.wid+10}}
				onClick={() => {
				    navigator.clipboard.writeText(item[0])
				    this.setState({copied: i})
				}}
			    >
                                <div 
				    className="word"
				    onMouseEnter={() => { if (this.state.hovering !== i) this.setState({hovering: i}) }}
				    onMouseLeave={() => { if (this.state.hovering === i) this.setState({hovering: -1}) }}
				>
				    <span 
					className="tooltip" 
					style={{
					    opacity: `${(this.state.hovering === i)? "1" : "0"}`, 
					    background: `${(this.state.copied === i)? "#148DE0" : "#454545"}`
					}}
				    >
					{(this.state.copied === i)? "copied!" : "copy"}
				    </span>
				    {item[0]}
				</div>
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
				//console.log(this.state.shown*10, this.state.data.length)
				if (this.props.shown*10 <= this.state.data.length) { 
				    this.props.setShown(this.props.shown + 1)
				    setTimeout(() => {
					if (this.more) {
					    this.more.current.scrollIntoView({
					    behavior: "smooth", 
					    block: "start",
					    })
					}
				    }, 0)
				}
                            }}
                        >
                            {this.moreIndicator()}
                        </p>
                    </div>
                </div>
                <div>
                    {this.loadingIndicator()}
                </div>
            </div>
        )
    }
}

export default Bars;
