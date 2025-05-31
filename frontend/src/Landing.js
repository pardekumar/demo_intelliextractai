import React from "react";
import botLogo from "./Pv-bot.gif";
import "./Landing.css";

const Landing = () => {
  return (
    <div className="landing-ai">
      <div className="landing-ai-card professional-theme">
        <img className="landing-ai-bot" src={botLogo} alt="AI Assistant Bot" />
        <h1 className="landing-ai-title">
          Welcome to{" "}
          <span className="brand-highlight">IntelliExtract AI</span>
        </h1>
        <p className="landing-ai-subtitle">
          Your intelligent assistant for document Q&amp;A.
        </p>
        <ul className="landing-ai-list">
          <li>
            <span className="list-icon">🔒</span>
            Upload your documents securely
          </li>
          <li>
            <span className="list-icon">⚡</span>
            Ask questions and get instant answers
          </li>
          <li>
            <span className="list-icon">🤖</span>
            Seamless, AI-powered experience
          </li>
        </ul>
        <div className="landing-ai-hint">
          <span>
            Start by{" "}
            <span className="hint-action">uploading a file</span> or{" "}
            <span className="hint-action">selecting one from the dropdown</span>.
          </span>
        </div>
      </div>
    </div>
  );
};

export default Landing;
