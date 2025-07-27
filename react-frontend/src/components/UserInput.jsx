import React, { useState } from 'react';
import { useChat } from '../context/ChatContext';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/chat';

export const UserInput = () => {
    const [inputValue, setInputValue] = useState('');
    const { state, dispatch } = useChat();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;

        const userMessage = {
            message_text: inputValue,
            message_source: 'user',
            created_at: new Date().toISOString(),
        };
        dispatch({ type: 'ADD_MESSAGE', payload: userMessage });
        dispatch({ type: 'START_LOADING' });

        try {
            const response = await axios.post(API_URL, {
                user_message: inputValue,
                session_id: state.sessionId,
            });

            const botMessage = {
                message_text: response.data.bot_response,
                message_source: 'bot',
                created_at: new Date().toISOString(),
            };
            dispatch({ type: 'ADD_MESSAGE', payload: botMessage });

            if (!state.sessionId) {
                dispatch({ type: 'SET_SESSION_ID', payload: response.data.session_id });
            }
        } catch (error) {
            console.error("Error sending message:", error);
            const errorMessage = {
                message_text: "Sorry, something went wrong. Please try again.",
                message_source: 'bot',
                created_at: new Date().toISOString(),
            };
            dispatch({ type: 'ADD_MESSAGE', payload: errorMessage });
        } finally {
            dispatch({ type: 'STOP_LOADING' });
        }

        setInputValue('');
    };

    return (
        <form onSubmit={handleSubmit} className="input-area">
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                disabled={state.isLoading}
            />
            <button type="submit" disabled={state.isLoading}>
                {state.isLoading ? '...' : 'Send'}
            </button>
        </form>
    );
};