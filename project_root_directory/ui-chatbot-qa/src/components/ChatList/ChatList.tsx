import React, { useEffect } from "react";
import { Box, Typography } from "@mui/material";
import "./ChatList.css";
import LinearProgress from "@mui/material/LinearProgress";
import { useAppContext } from "../../context/AppContext";

const ChatList: React.FC = () => {
  const { state } = useAppContext();

  useEffect(() => {}, [state]);

  return (
    <Box className="chat-list">
      {state.messages.map((chat, index) => (
        <Box key={index} className="chat-message">
          {chat.message && (
            <Typography
              variant="body1"
              sx={{
                whiteSpace: "normal",
                overflowWrap: "break-word",
              }}
            >
              {chat.message}
            </Typography>
          )}
          {chat.response && (
            <Typography
              variant="body1"
              className="chat-response"
              sx={{
                whiteSpace: "normal",
                overflowWrap: "break-word",
              }}
            >
              {chat.response}
            </Typography>
          )}
        </Box>
      ))}
      {state.isLoading && (
        <Box>
          <LinearProgress color="inherit" sx={{ width: "40%" }} />
        </Box>
      )}
    </Box>
  );
};

export default ChatList;
