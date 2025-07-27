import React, { useRef, useEffect } from 'react';
import { useChat } from '../context/ChatContext';
import { Message } from './Message';

export const MessageList = () => {
    const { state } = useChat();
    const endOfMessagesRef = useRef(null);

    // Automatically scroll to the bottom when new messages are added
    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [state.messages]);

    return (
        <div className="response-area">
            {state.messages.map((msg, index) => (
                <Message key={index} message={msg} />
            ))}
            {state.isLoading && <div className="message bot-message">...</div>}
            <div ref={endOfMessagesRef} />
        </div>
    );
};