import React from 'react';
import { Link } from 'react-router-dom';

export const Navigation = () => {
    return (
        <nav style={{ padding: '20px', background: '#f4f4f4' }}>
            <Link to="/" style={{ marginRight: '20px' }}>Dashboard</Link>
            <Link to="/users">Users</Link>
        </nav>
    );
};
