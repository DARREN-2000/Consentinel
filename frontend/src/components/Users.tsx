import React, { useEffect, useState } from 'react';
import axios from 'axios';

export const Users = () => {
    const [users, setUsers] = useState<any[]>([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/users').then(res => setUsers(res.data.users)).catch(console.error);
    }, []);

    return (
        <div style={{ padding: '20px' }}>
            <h1>Users</h1>
            <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
                <thead>
                    <tr>
                        <th>Email</th>
                        <th>Lifecycle Stage</th>
                        <th>Fatigue Score</th>
                        <th>Intent Score</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(u => (
                        <tr key={u.id} style={{ borderBottom: '1px solid #ccc' }}>
                            <td>{u.email}</td>
                            <td>{u.lifecycle_stage}</td>
                            <td>{u.fatigue_score}</td>
                            <td>{u.intent_score}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};
