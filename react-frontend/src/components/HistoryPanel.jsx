import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useChat } from '../context/ChatContext';

const API_URL = 'http://127.0.0.1:8000';

export const HistoryPanel = () => {
    const [sessions, setSessions] = useState([]);
    const { dispatch } = useChat();
    const userId = '123'; // Hardcoded for now, would come from login in a real app

    useEffect(() => {
        const fetchSessions = async () => {
            try {
                const response = await axios.get(`${API_URL}/api/sessions/${userId}`);
                setSessions(response.data.session_ids);
            } catch (error) {
                console.error('Failed to fetch sessions:', error);
            }
        };
        fetchSessions();
    }, []);

    const loadSession = async (sessionId) => {
        try {
            const response = await axios.get(`${API_URL}/api/history/${sessionId}`);
            dispatch({ type: 'SET_MESSAGES', payload: response.data });
            dispatch({ type: 'SET_SESSION_ID', payload: sessionId });
        } catch (error) {
            console.error('Failed to load session history:', error);
        }
    };

    return (
        <div className="history-panel">
            <h3>Past Conversations</h3>
            <ul>
                {sessions.map((sessionId) => (
                    <li key={sessionId} onClick={() => loadSession(sessionId)}>
                        Session: {sessionId.substring(0, 8)}...
                    </li>
                ))}
            </ul>
        </div>
    );
};