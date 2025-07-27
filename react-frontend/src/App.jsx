import React from 'react';
import { ChatProvider } from './context/ChatContext';
import { ChatWindow } from './components/ChatWindow';
import './App.css'; // We'll create this file next

function App() {
    return (
        <ChatProvider>
            <main>
                <ChatWindow />
            </main>
        </ChatProvider>
    );
}

export default App;