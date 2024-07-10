import { Box, Toolbar } from "@mui/material";
import ChatList from "../ChatList/ChatList";
import ChatInput from "../ChatInput/ChatInput";

interface ChatBoxProps {
  handleSendMessage: (message: string) => void;
}

export default function ChatBox({
  handleSendMessage,
}: ChatBoxProps) {
  return (
    <Box
      component="main"
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        overflow: "hidden",
      }}
    >
      <Toolbar />
      <Box sx={{ overflowY: "auto", width: "100%", height: "90%" }}>
        <ChatList />
      </Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          mt: "auto",
          width: "100%",
          p: 2,
          maxWidth: 600,
          margin: "auto",
          position: "sticky",
          bottom: 0,
        }}
      >
        <ChatInput onSendMessage={handleSendMessage} />
      </Box>
    </Box>
  );
}
