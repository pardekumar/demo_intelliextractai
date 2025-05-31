// ChatInterface.js
import React, { useState } from "react";

const ChatInterface = ({ botResponse }) => {
  const [userMessage, setUserMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const handleSendMessage = () => {
    // Send user message to chatbot and update chat history
    setChatHistory([...chatHistory, { message: userMessage, sender: "user" }]);
    // You'll need to replace this with actual logic to get bot response
    setChatHistory([...chatHistory, { message: botResponse, sender: "bot" }]);
    setUserMessage("");
  };

  return (
    <div>
      <div>
        {chatHistory.map((chat, index) => (
          <div key={index}>
            {chat.sender === "user" ? "You: " : "Bot: "}
            {chat.message}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={userMessage}
        onChange={(e) => setUserMessage(e.target.value)}
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default ChatInterface;
