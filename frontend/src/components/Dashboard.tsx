import { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export const Dashboard = () => {
    const [summary, setSummary] = useState<any>({});
    const [fatigue, setFatigue] = useState<any[]>([]);
    const [channels, setChannels] = useState<any[]>([]);
    const [suppression, setSuppression] = useState<any[]>([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/analytics/summary')
            .then(res => setSummary(res.data))
            .catch(err => {
                console.error("API failed, using mock data", err);
                setSummary({
                    total_users: 120,
                    total_decisions: 500,
                    suppression_rate: 0.15,
                    avg_intent_score: 0.75,
                    avg_churn_risk: 0.2,
                    avg_fatigue_score: 0.3,
                    activated_users: 80,
                    activation_rate: 0.66
                });
            });

        axios.get('http://localhost:8000/api/analytics/fatigue')
            .then(res => setFatigue(res.data))
            .catch(err => {
                console.error("API failed, using mock data", err);
                setFatigue([
                    { bucket: "0.0-0.2", count: 50, percentage: 0.4 },
                    { bucket: "0.2-0.4", count: 40, percentage: 0.3 },
                    { bucket: "0.4-0.6", count: 20, percentage: 0.15 },
                    { bucket: "0.6-0.8", count: 10, percentage: 0.1 },
                    { bucket: "0.8-1.0", count: 0, percentage: 0.0 }
                ]);
            });

        axios.get('http://localhost:8000/api/analytics/channels')
            .then(res => setChannels(res.data))
            .catch(err => {
                console.error("API failed, using mock data", err);
                setChannels([
                    { channel: "email", total_decisions: 300, suppressed: 50, open_rate: 0.25, click_rate: 0.1 },
                    { channel: "sms", total_decisions: 150, suppressed: 20, open_rate: 0.8, click_rate: 0.15 },
                    { channel: "push", total_decisions: 50, suppressed: 5, open_rate: 0.5, click_rate: 0.05 }
                ]);
            });

        axios.get('http://localhost:8000/api/analytics/suppression')
            .then(res => setSuppression(res.data))
            .catch(err => {
                console.error("API failed, using mock data", err);
                setSuppression([
                    { reason: "no_consent", count: 40, percentage: 0.5 },
                    { reason: "fatigue", count: 25, percentage: 0.3 },
                    { reason: "quiet_hours", count: 10, percentage: 0.12 },
                    { reason: "unsubscribed", count: 5, percentage: 0.08 }
                ]);
            });
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
                    <p>{summary.suppression_rate !== undefined ? (summary.suppression_rate * 100).toFixed(2) + "%" : ""}</p>
                </div>
            </div>

            <div style={{ display: 'flex', gap: '40px', flexWrap: 'wrap' }}>
                <div>
                    <h2>Fatigue Distribution</h2>
                    <BarChart width={400} height={300} data={fatigue}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="bucket" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="count" fill="#8884d8" />
                    </BarChart>
                </div>

                <div>
                    <h2>Channel Performance</h2>
                    <BarChart width={400} height={300} data={channels}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="channel" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="total_decisions" fill="#82ca9d" name="Total Decisions" />
                        <Bar dataKey="suppressed" fill="#ff7f50" name="Suppressed" />
                    </BarChart>
                </div>

                <div>
                    <h2>Suppression Reasons</h2>
                    <BarChart width={400} height={300} data={suppression}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="reason" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="count" fill="#ff4500" name="Count" />
                    </BarChart>
                </div>
            </div>
        </div>
    );
};
