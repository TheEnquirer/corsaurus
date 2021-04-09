import './App.css';
import Bars from './components/bars.jsx';
import Search from './components/search.jsx';

function App() {
  return (
    <div className="main">
	<Search />
	<div className="over-bars">
	    <Bars />
	</div>
    </div>
  );
}

export default App;
