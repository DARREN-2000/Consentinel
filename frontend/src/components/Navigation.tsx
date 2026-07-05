import { Link } from 'react-router-dom';

export const Navigation = () => {
    return (
        <nav style={{ padding: '20px', background: '#f4f4f4' }}>
            <Link to="/" style={{ marginRight: '20px' }}>Dashboard</Link>
            <Link to="/users" style={{ marginRight: '20px' }}>Users</Link>
            <Link to="/audiences" style={{ marginRight: '20px' }}>Audiences</Link>
            <Link to="/journeys" style={{ marginRight: '20px' }}>Journeys</Link>
            <Link to="/decisions" style={{ marginRight: '20px' }}>Decisions</Link>
            <Link to="/consents" style={{ marginRight: '20px' }}>Consents</Link>
            <Link to="/events" style={{ marginRight: '20px' }}>Events</Link>
            <Link to="/experiments">Experiments</Link>
        </nav>
    );
};
