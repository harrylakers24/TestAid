import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const URL = 'url';
const PROMPT = 'prompt';

const RealTimeComponent = () => {
    const [prompt, setPrompt] = useState('');
    const [url, setUrl] = useState('');
    const [socket, setSocket] = useState(null);
    // Adding a state to track reconnection attempts
    const [reconnectAttempt, setReconnectAttempt] = useState(0);
    const [explanation, setExplanation] = useState('Empty');

    const handleLiveFeedback = (data) => {
        setExplanation(data);
    }

    useEffect(() => {
        // Creating a new socket connection
        const newSocket = io('ws://127.0.0.1:5000');
        newSocket.on('connect', () => {
            console.log('Connected');
        });

        newSocket.on('disconnect', () => {
            console.log('Disconnected');
        });

        newSocket.on('liveFeedback', handleLiveFeedback);

        setSocket(newSocket);

        // Cleanup function to disconnect the socket when the component unmounts or before reconnecting
        return () => {
            newSocket.disconnect();
        };
    }, [reconnectAttempt]); // Re-run this effect when `reconnectAttempt` changes

    const onChange = (category, value) => {
        if (category === PROMPT) {
            setPrompt(value);
        } else if (category === URL) {
            setUrl(value);
        }
    };

    const onClick = () => {
        if (socket) {
            socket.emit('prompt', { prompt, url });
        }
    };

    // Revised reconnect function
    const reconnect = () => {
        setReconnectAttempt((prevAttempt) => prevAttempt + 1);
    }

    return (
        <div>
            <h1>Real Time Component</h1>
            <input onChange={(e) => onChange(PROMPT, e.target.value)} type="text" placeholder="Enter your prompt" />
            <input onChange={(e) => onChange(URL, e.target.value)} type="text" placeholder="Enter your URL" />
            <button onClick={onClick}>Submit</button>
            <button onClick={reconnect}>Reconnect</button>
            <p>{explanation}</p>
        </div>
    );
};

export default RealTimeComponent;
