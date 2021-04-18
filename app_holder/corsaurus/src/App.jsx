import React, { Component } from 'react';
import './App.css';
import Bars from './components/bars.jsx';
import Search from './components/search.jsx';
import autoBind from 'react-autobind';

class App extends Component 
{
    constructor(props) 
    {
	super(props);
	autoBind(this);

	this.state = { 
	    data: [],
	    anim: "",
	    shown: 1,
	};
    }

    componentDidMount() {}

    setData(data) 
    {
	//console.log("setting", data)
	this.setState({ data: data });
	//console.log(this.state.data)
    }

    setShown(num) {
	this.setState({shown: num})
    }

    render() 
    {
	//<a className="help-button" href="help">Help</a>
	return (
	    <div className="main">
		<div className="sticky-top">
		    <h1
			onMouseEnter={() => this.setState({anim: "slide-anim"})}
			onMouseLeave={() => this.setState({anim: ""})}
			>Corsaurus</h1>
		    <p
			onMouseEnter={() => this.setState({anim: "slide-anim"})}
			onMouseLeave={() => this.setState({anim: ""})}
            className={`slideout ${this.state.anim}`}>/kôrˈsôrəs/ <br/>
            <a href={"https://github.com/theenquirer/corsaurus"}>Made with ❤️</a> by Enquirer, FlyN-Nick, and Exr0n.</p>
		    <div style={{display: "flex", alignItems: "center", justifyContent: "center"}}>
			<Search
			    set={this.setData}
			    setShown={this.setShown}
			/>
		    </div>
		</div>
		<div className="over-bars">
		    <Bars data={this.state.data} shown={this.state.shown} setShown={this.setShown}/>
		</div>
	    </div>
	)
	//<footer className="footer">
	//    <div className="footer-text">
	//        <p>
	//            <a href="/help">help</a>&nbsp;|&nbsp;
	//            <a href="https://github.com/TheEnquirer/corsaurus">source</a> 
	//            &nbsp;| ❤️ <a href="https://github.com/FlyN-Nick">FlyN-Nick</a> <a href="https://github.com/TheEnquirer">TheEnquirer</a> <a href="https://github.com/Exr0n">Exr0n</a>
	//        </p>
	//    </div>
	//</footer>
    }
}

export default App;
