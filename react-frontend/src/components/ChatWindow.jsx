// No changes to imports
import React from 'react';
import { MessageList } from './MessageList';
import { UserInput } from './UserInput';
import { HistoryPanel } from './HistoryPanel';

export const ChatWindow = () => {
    return (
        // ADD the new "app-layout" div
        <div className="app-layout"> 
            <HistoryPanel />
            <div className="chat-container">
                <div className="chat-header">E-Commerce Support</div>
                <MessageList />
                <UserInput />
            </div>
        </div>
    );
};