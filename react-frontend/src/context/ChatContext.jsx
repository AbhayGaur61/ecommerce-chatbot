import React, { createContext, useReducer, useContext } from 'react';

// Initial state for our chat
const initialState = {
    messages: [],
    isLoading: false,
    sessionId: null,
};

// The reducer function handles state changes
const chatReducer = (state, action) => {
    switch (action.type) {
        case 'START_LOADING':
            return { ...state, isLoading: true };
        case 'STOP_LOADING':
            return { ...state, isLoading: false };
        case 'SET_MESSAGES':
            return { ...state, messages: action.payload };
        case 'ADD_MESSAGE':
            return { ...state, messages: [...state.messages, action.payload] };
        case 'SET_SESSION_ID':
            return { ...state, sessionId: action.payload };
        default:
            return state;
    }
};

// Create the context
const ChatContext = createContext();

// The provider component will wrap our application
export const ChatProvider = ({ children }) => {
    const [state, dispatch] = useReducer(chatReducer, initialState);

    return (
        <ChatContext.Provider value={{ state, dispatch }}>
            {children}
        </ChatContext.Provider>
    );
};

// A custom hook to easily access the context
export const useChat = () => {
    return useContext(ChatContext);
};