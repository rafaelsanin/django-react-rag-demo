import React, { useState } from "react";
import "./App.css";
import { Box, CssBaseline, ThemeProvider } from "@mui/material";
import theme from "./theme";
import ResponsiveDrawer from "./components/ResponsiveDrawer/ResponsiveDrawer";
import ResponsiveAppBar from "./components/ResponsiveAppBar/ResponsiveAppBar";
import ChatBox from "./components/ChatBox/ChatBox";
import useSendMessage from "./hooks/useSendMessage";

const App: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isClosing, setIsClosing] = useState(false);
  const { handleSendMessage } = useSendMessage();

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <ResponsiveAppBar
          isClosing={isClosing}
          mobileOpen={mobileOpen}
          setMobileOpen={setMobileOpen}
        />
        <ResponsiveDrawer
          isClosing={isClosing}
          mobileOpen={mobileOpen}
          setIsClosing={setIsClosing}
          setMobileOpen={setMobileOpen}
        />
        <Box sx={{ flexGrow: 1 }}>
          <ChatBox handleSendMessage={handleSendMessage} />
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;
