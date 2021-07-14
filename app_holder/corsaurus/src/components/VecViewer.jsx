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
            data: this.props.data,
            mounted: false,
            //shown: 1,
            loading: true,
            hovering: -1,
            copied: -1,
        };

    }


    componentDidMount() {
        this.setState({mounted: true});
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

