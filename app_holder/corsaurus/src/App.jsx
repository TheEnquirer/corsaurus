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

        this.state = { data: [] };
    }

    componentDidMount() {}
    
    setData(data) 
	{
		//console.log("setting", data)
		this.setState({ data: data });
		//console.log(this.state.data)
    }

    render() 
	{
		return (
			<div className="main">
				<a className="help-button" href="help">Help</a>
				<div className="sticky-top">
                    <h1>Corsaurus</h1>
				    <div style={{display: "flex", alignItems: "center", justifyContent: "center"}}>
					<Search
						set={this.setData}
					/>
				    </div>
				</div>
				<div className="over-bars">
					<Bars data={this.state.data}/>
				</div>
			</div>
		)
		/*
		<footer className="footer">
			<div className="footer-text">
				<p>
					&copy; Developed with ❤️ by <a href="https://github.com/FlyN-Nick">FlyN-Nick</a>, <a href="https://github.com/TheEnquirer">TheEnquirer</a>, and <a href="https://github.com/Exr0n">Exr0n</a>.
					Check out the source code <a href="https://github.com/TheEnquirer/corsaurus">here</a>.
				</p>
			</div>
		</footer>
		*/
    }
}

export default App;
