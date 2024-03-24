import React, { useEffect, useState } from "react";
import io from "socket.io-client";

const URL = "url";
const PROMPT = "prompt";

const Pages = {
  START: "Start",
  PROMPT: "Promt",
  RESULT: "Result",
};

const RealTimeComponent = () => {
  const [prompt, setPrompt] = useState("");
  const [url, setUrl] = useState("");
  const [socket, setSocket] = useState(null);
  // Adding a state to track reconnection attempts
  const [reconnectAttempt, setReconnectAttempt] = useState(0);
  const [debug, setDebug] = useState(false); // Added debug state
  const [currentPage, setCurrentPage] = useState(Pages.START); // State to track the current page

  useEffect(() => {
    // Creating a new socket connection
    const newSocket = io("ws://127.0.0.1:5000");
    newSocket.on("connect", () => {
      console.log("Connected");
    });

    newSocket.on("disconnect", () => {
      console.log("Disconnected");
    });

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
      socket.emit("prompt", { prompt, url });
    }
  };

  // Revised reconnect function
  const reconnect = () => {
    setReconnectAttempt((prevAttempt) => prevAttempt + 1);
  };

  return (
    <div>
      {currentPage === Pages.START && (
        <div>
          <img
            src="../images/image.png"
            alt="Description"
            className="logo-image"
          />

          <button
            onClick={() => setCurrentPage(Pages.PROMPT)}
            className="submit-button"
          >
            Start Here
          </button>
        </div>
      )}
      {currentPage === Pages.PROMPT && (
        <div>
          <img
            src="../images/image.png"
            alt="Description"
            className="logo-image"
          />
          <div className="input-container">
            <h1 className="instruction-text">
              Enter the link and prompt you wish to test
            </h1>
            <input
              onChange={(e) => onChange(PROMPT, e.target.value)}
              type="text"
              placeholder="Enter your prompt"
              className="text-box"
            />
            <input
              onChange={(e) => onChange(URL, e.target.value)}
              type="text"
              placeholder="Enter your URL"
              className="text-box"
            />
            <button onClick={onClick} className="submit-button">
              Generate
            </button>
          </div>
          {debug && (
            <button onClick={reconnect} className="submit-button">
              Reconnect
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default RealTimeComponent;
