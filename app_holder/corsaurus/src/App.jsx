//import './App.css';
//import React, { useState } from 'react';
//import Bars from './components/bars.jsx';
//import Search from './components/search.jsx';

////let once = true
//function handleNewData(data, set) {
//    //if (once == true) {
//        set(data)
//        //once = false
//    //}
//}

//function App() {
//    //const [isData, setData] = useState([["test", 0.5]]);
//    const [isData, setData] = useState(false);
//    let newdata = [["nottest", 0.7]]
//    //if (once) { setData(newdata); once = false }
//    handleNewData(newdata, setData)
//    console.log(isData, "new")

//    return (
//    <div className="main">
//        <Search set={(content) => {
//            //console.log("setter", content)
//            //setData(content)
//            console.log("data", isData)
//            handleNewData(content, useState)

//    }}/>
//        <div className="over-bars">
//            <Bars data={isData}/>
//        </div>
//    </div>
//  );
//}

//import { chevronForwardCircle, checkmarkCircle, filterOutline, listOutline, bicycle } from 'ionicons/icons';
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
	    //data: [['test', 0.5]]
	    data: [],
	}
    }

    componentDidMount() {}
    
    setData(data) {
	console.log("setting", data)
	this.setState({data: data})
	console.log(this.state.data)
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
