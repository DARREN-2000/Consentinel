import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export const Dashboard = () => {
    const [summary, setSummary] = useState<any>({});
    const [fatigue, setFatigue] = useState<any[]>([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/analytics/summary').then(res => setSummary(res.data)).catch(console.error);
        axios.get('http://localhost:8000/api/analytics/fatigue').then(res => setFatigue(res.data)).catch(console.error);
    }, []);

    return (
        <div style={{ padding: '20px' }}>
            <h1>Consentinel Dashboard</h1>
            <div style={{ display: 'flex', gap: '20px', marginBottom: '40px' }}>
                <div style={{ border: '1px solid #ccc', padding: '20px' }}>
                    <h3>Total Users</h3>
                    <p>{summary.total_users}</p>
                </div>
                <div style={{ border: '1px solid #ccc', padding: '20px' }}>
                    <h3>Total Decisions</h3>
                    <p>{summary.total_decisions}</p>
                </div>
                <div style={{ border: '1px solid #ccc', padding: '20px' }}>
                    <h3>Suppression Rate</h3>
                    <p>{(summary.suppression_rate * 100).toFixed(2)}%</p>
                </div>
            </div>

            <h2>Fatigue Distribution</h2>
            <BarChart width={500} height={300} data={fatigue}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="bucket" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
        </div>
    );
};
