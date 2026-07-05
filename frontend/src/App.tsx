import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { Dashboard } from './components/Dashboard';
import { Users } from './components/Users';
import { Audiences } from './components/Audiences';
import { Journeys } from './components/Journeys';
import { Decisions } from './components/Decisions';
import { Consents } from './components/Consents';
import { Events } from './components/Events';
import { Experiments } from './components/Experiments';
import { Navigation } from './components/Navigation';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/users" element={<Users />} />
          <Route path="/audiences" element={<Audiences />} />
          <Route path="/journeys" element={<Journeys />} />
          <Route path="/decisions" element={<Decisions />} />
          <Route path="/consents" element={<Consents />} />
          <Route path="/events" element={<Events />} />
          <Route path="/experiments" element={<Experiments />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
