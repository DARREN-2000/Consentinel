import { useEffect, useState } from 'react';
import axios from 'axios';

export const Users = () => {
    const [users, setUsers] = useState<any[]>([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/users')
            .then(res => setUsers(res.data.users))
            .catch(err => {
                console.error("API failed, using mock data", err);
                setUsers([
                    { id: 1, email: "john@example.com", lifecycle_stage: "Active", fatigue_score: 25, intent_score: 0.8 },
                    { id: 2, email: "jane@example.com", lifecycle_stage: "At Risk", fatigue_score: 85, intent_score: 0.2 },
                    { id: 3, email: "bob@example.com", lifecycle_stage: "New", fatigue_score: 10, intent_score: 0.9 },
                    { id: 4, email: "alice@example.com", lifecycle_stage: "Active", fatigue_score: 60, intent_score: 0.5 },
                    { id: 5, email: "charlie@example.com", lifecycle_stage: "Dormant", fatigue_score: 95, intent_score: 0.1 }
                ]);
            });
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
