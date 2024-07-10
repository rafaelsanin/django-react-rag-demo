import React, { useState } from "react";
import { IconButton, InputBase, Paper } from "@mui/material";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import SendIcon from "@mui/icons-material/Send";
import "./ChatInput.css";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (message.trim() !== "") {
      onSendMessage(message.trim());
      setMessage("");
    }
  };

  return (
    <Paper component="form" className="chat-input" onSubmit={handleSubmit}>
      <IconButton className="icon-button" aria-label="attach file">
        <AttachFileIcon className="icon" />
      </IconButton>
      <InputBase
        className="input-base"
        placeholder="Message RAG Q&A chatbot"
        inputProps={{ "aria-label": "message rag qa chatbot" }}
        value={message}
        onChange={handleInputChange}
      />
      <IconButton type="submit" className="icon-button" aria-label="send">
        <SendIcon className="icon" />
      </IconButton>
    </Paper>
  );
};

export default ChatInput;
