// ChatApp.js
import React, { useState } from "react";
import Skeleton from "@mui/material/Skeleton";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Typewriter from "../TypeWriter";
import VerticalLinearStepper from "../Stepper";
import SideBar from "../SideBar";
import botLogo from "../../Pv-bot.gif";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import CircularProgress from "@mui/material/CircularProgress";

import "./ChatApp.css";

const modalStyle = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 600,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
  overflow: "auto",
};

const assistantMessage = [
  {
    text: "Hi. I'm your AI assistant ... Let me know how can i help you",
    sender: "bot",
  },
];

const ChatApp = (props) => {
  const {
    messages,
    inputText,
    setMessages,
    setInputText,
    summary,
    isSummaryLoading,
    isSummaryGenerating,
    toogleSummary,
    setToogleSummary,
  } = props;
  const [citiations, SetCitiations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false);
  // const [summary, setSummary] = useState([]);

  const handleOpen = (citiations) => {
    SetCitiations(citiations);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);

  const fetchLlm = async (inputText1) => {
    try {
      setIsLoading(true);
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/documents/ask`,
        {
          method: "POST",
          body: JSON.stringify({
            prompt: inputText1.trim(),
            files: [props.pdfFile.name],
          }),
          headers: {
            Accept: "application/json",
            "content-type": "application/json",
          },
        }
      );
      const res = await response.json();
      setMessages((prev) => [
        ...prev,
        // {
        //   text: res.message.output_text,
        //   inputDocument: res.message.input_documents,
        //   sender: "bot",
        // },
        {
          text: res.message.result,
          inputDocument: res.message.source_documents,
          sender: "bot",
        },
      ]);
      setIsLoading(false);
    } catch (e) {
      console.log("error", e);
      setIsLoading(false);
    }
  };

  const handleSendMessage = () => {
    if (inputText.trim() !== "") {
      setMessages((prev) => [...prev, { text: inputText, sender: "user" }]);
      fetchLlm(inputText.trim());
      // handleStreamSummary(inputText.trim());
      setInputText("");
      // Call a function to get bot response here
      // For now, just simulating a bot response after 1 second
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {(!toogleSummary || (isSummaryLoading && summary.length === 0)) && (
          <div className="summary-button">
            <Button
              className="citation"
              variant="contained"
              size="small"
              startIcon={
                isSummaryLoading ? (
                  <CircularProgress style={{ color: "#fff" }} size="1.2rem" />
                ) : (
                  <PictureAsPdfIcon color="inherit" />
                )
              }
              onClick={() => setToogleSummary(true)}
              sx={{
                backgroundColor: (theme) => theme.palette.secondary.main, // Use header theme color
                color: (theme) => theme.palette.secondary.contrastText,
                "&:hover": {
                  backgroundColor: (theme) => theme.palette.secondary.dark,
                },
                borderRadius: 2,
                boxShadow: 2,
                textTransform: "none",
                fontWeight: 600,
                fontSize: "1rem",
                paddingX: 2,
                paddingY: 1,
              }}
            >
              Extract Information
            </Button>
          </div>
        )}
        {summary && summary.length && (
          <SideBar
            summary={summary}
            isSummaryLoading={isSummaryLoading}
            isSummaryGenerating={isSummaryGenerating}
          />
        )}
        {messages.map((message, index) =>
          message.sender === "bot" ? (
            <div key={index} className={`message ${message.sender}`}>
              <div>
                <Typewriter text={message.text} delay={10} />
              </div>
              {message.inputDocument && (
                <Button
                  className="citation"
                  variant="outlined"
                  size="small"
                  onClick={() => handleOpen(message.inputDocument)}
                >
                  Citation
                </Button>
              )}
            </div>
          ) : (
            <div key={index} className={`message ${message.sender}`}>
              {message.text}
            </div>
          )
        )}
        {isLoading && <Skeleton variant="rounded" width="80%" height={60} />}
      </div>
      {
        <div className="chat-input">
          <div style={{ display: "flex", alignItems: "center" }}>
            <img className="assistant" src={botLogo} alt="bot" />
            {assistantMessage.map((message, index) =>
              message.sender === "bot" ? (
                <div key={index} className={`assistant-text`}>
                  <div>
                    <Typewriter text={message.text} delay={10} />
                  </div>
                </div>
              ) : (
                <div key={index} className={`message ${message.sender}`}>
                  {message.text}
                </div>
              )
            )}
          </div>
          <div style={{ display: "flex" }}>
            <input
              type="text"
              placeholder="Type a message..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleSendMessage();
                }
              }}
            />
            <Button
              variant="contained"
              size="medium"
              onClick={handleSendMessage}
              sx={{
                backgroundColor: (theme) => theme.palette.secondary.main, // Match header theme
                color: (theme) => theme.palette.secondary.contrastText,
                "&:hover": {
                  backgroundColor: (theme) => theme.palette.secondary.dark,
                },
                borderRadius: 2,
                boxShadow: 2,
                textTransform: "none",
                fontWeight: 600,
                fontSize: "1rem",
                paddingX: 3,
                paddingY: 1,
                marginLeft: 1,
              }}
            >
              Send
            </Button>
          </div>
        </div>
      }
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
        style={{
          overflow: "auto",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Box sx={modalStyle}>
          <VerticalLinearStepper inputDocument={citiations} />
        </Box>
      </Modal>
    </div>
  );
};

export default ChatApp;
