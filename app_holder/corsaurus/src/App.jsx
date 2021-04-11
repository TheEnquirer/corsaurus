import React, { Component } from 'react';
import './App.css';
import Bars from './components/bars.jsx';
import Search from './components/search.jsx';
import autoBind from 'react-autobind';

class App extends Component {
    constructor(props) {
        super(props);
        autoBind(this);

        this.state = {
	    data: [],
	}
    }

    componentDidMount() {}
    
    setData(data) {
	//console.log("setting", data)
	this.setState({data: data})
	//console.log(this.state.data)
    }

    render() {
	return (
	    <div className="main">
		<Search
		    set={this.setData}
		/>
		<div className="over-bars">
		    <Bars data={this.state.data}/>
		</div>
	    </div>

	)
    }
}

export default App;
