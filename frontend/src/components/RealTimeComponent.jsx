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

  const [explanation, setExplanation] = useState([]);

  const handleLiveFeedback = (data) => {
    setExplanation((explanation) => [...explanation, data]);
  };

  useEffect(() => {
    // Creating a new socket connection
    const newSocket = io("ws://127.0.0.1:5000");
    newSocket.on("connect", () => {
      console.log("Connected");
    });

    newSocket.on("disconnect", () => {
      console.log("Disconnected");
    });

    newSocket.on("liveFeedback", handleLiveFeedback);

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
      <img
        src={require("../images/image.png")}
        alt="Description"
        className="logo-image"
      />

      {currentPage === Pages.START && (
        <div>
          <div className="test-aid-container">
            <div className="speech-bubble">
              <p className="instruction-text">
                Hi there! 👋 I'm TestAid, your AI-driven companion for user
                testing. By mimicking user interactions, I help evaluate digital
                products by pin-pointing issues and providing feedback to
                enhance the user experience.
              </p>
            </div>
            <img
              src={require("../images/BigRobot.png")}
              alt="Description"
              className="big-robot-image"
            />
            <button
              onClick={() => setCurrentPage(Pages.PROMPT)}
              className="submit-button"
            >
              Start Here
            </button>
            <div>
              {explanation.map((exp, index) => (
                <p key={index}>{exp}</p>
              ))}
            </div>
          </div>
        </div>
      )}
      {currentPage === Pages.PROMPT && (
        <div>
          <img
            src={require("../images/image.png")}
            alt="Description"
            className="logo-image"
          />
          <img
            src={require("../images/BigRobot.png")}
            alt="Description"
            className="big-robot-image"
          />
          <div className="input-container">
            <h1 className="instruction-text">
              Enter the link and prompt you wish to test:
            </h1>
            <input
              onChange={(e) => onChange(PROMPT, e.target.value)}
              type="text"
              placeholder="prompt:"
              className="text-box"
            />
            <input
              onChange={(e) => onChange(URL, e.target.value)}
              type="text"
              placeholder="link:"
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
