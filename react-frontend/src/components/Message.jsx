import React from 'react';

export const Message = ({ message }) => {
    // Determines the CSS class based on who sent the message
    const messageClass = message.message_source === 'user' ? 'user-message' : 'bot-message';

    return (
        <div className={`message ${messageClass}`}>
            <p>{message.message_text}</p>
        </div>
    );
};