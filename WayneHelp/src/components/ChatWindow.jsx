import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ChatWindow.css";

const ChatWindow = () => {
  const navigate = useNavigate();

  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");

  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages([...messages, { sender: "user", text: input }]);
      setInput("");
    }
  };

  const handleSaveChat = () => {
    const chatContent = messages
      .map((msg) => `${msg.sender === "bot" ? "Bot" : "You"} : ${msg.text}}`)
      .join("\n");
    const blob = new Blob([chatContent], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "chat.txt";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleBookAppointment = () => {
    navigate("/appointment");
  };

  return (
    <div className="chat-window-container">
      <header className="chat-header">
        <h1>Book Appointment</h1>
        <div className="header-buttons">
          <button onClick={handleSaveChat}>Save Chat as Text</button>
          <button onClick={handleBookAppointment}>Book Appopintment</button>
        </div>
      </header>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${
              msg.sender === "bot" ? "bot-message" : "user-message"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <footer className="chat-footer">
        <input
          type="text"
          placeholder="Type here..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={handleSendMessage}>Send</button>
      </footer>
    </div>
  );
};

export default ChatWindow;
