import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import IntroBubble from "../images/intro-text-bubble.svg";

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
  const [debug, setDebug] = useState(true); // Added debug state
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
      setCurrentPage(Pages.RESULT);
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
            {/* <div className="speech-bubble">
              <p className="instruction-text">
                Hi there! 👋 I'm TestAid, your AI-driven companion for user
                testing. By mimicking user interactions, I help evaluate digital
                products by pin-pointing issues and providing feedback to
                enhance the user experience.
              </p>
            </div> */}
          <svg width="749" height="417" viewBox="0 0 749 417" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M63.375 345.194C63.375 334.778 58.965 319.927 58.965 319.927L100.854 323.298C100.854 323.298 93.5381 339.061 87.6704 347.149C76.0457 363.172 34.4527 411.589 34.4527 411.589C34.4527 411.589 63.375 370.735 63.375 345.194Z" stroke="black" stroke-width="2.5"/>
            <rect x="1" y="1" width="747" height="324.723" rx="41" fill="#FFFDFD" stroke="black" stroke-width="2"/>
            <path d="M61.0491 321.58L99.7937 322.18L96.8413 328.309H62.694L61.0491 321.58Z" fill="white"/>
            <text fill="black" style={{"white-space": 'pre'}} font-family="HK Grotesk" font-size="35" letter-spacing="0em"><tspan x="488.728" y="118.519">By mimicking </tspan><tspan x="55.2954" y="158.519">user interactions, I help evaluate digital </tspan><tspan x="55.2954" y="198.519">products by pin-pointing issues and </tspan><tspan x="55.2954" y="238.519">providing feedback to enhance the user </tspan><tspan x="55.2954" y="278.519">experience.</tspan></text>
            <text fill="black" style={{"white-space": 'pre'}} font-family="HK Grotesk" font-size="35" letter-spacing="0em"><tspan x="479.158" y="118.519"> </tspan></text>
            <text fill="black" style={{"white-space": 'pre'}} font-family="HK Grotesk" font-size="35" letter-spacing="0em"><tspan x="55.2954" y="78.519">Hi there! &#x1f44b; I&#x2019;m TestAid, your AI-driven </tspan><tspan x="55.2954" y="118.519">companion for user testing.</tspan></text>
          </svg>
            <img
              src={require("../images/big-robot.png")}
              alt="Robot Mascot"
              className="big-robot-image"
            />
            <button
              onClick={() => setCurrentPage(Pages.PROMPT)}
              className="submit-button"
            >
              start here
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
      {currentPage === Pages.RESULT && (
        <>
          <div className="results-layout-container">
            {/* Left side content */}
            <div className="results-content">
              <div className="speech-bubble">
                <p className="instruction-text">
                  Here are the results of the test. Click the button below to start a new test.
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
                New Test
              </button>
            </div>
            
            <div className="explanation-container">
              {explanation.map((exp, index) => (
                <p className="response-bubble" key={index}>{exp}</p>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default RealTimeComponent;
