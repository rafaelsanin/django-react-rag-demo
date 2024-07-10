import { useAppContext } from "../context/AppContext";
import { ChatMessage } from "../types";

const useSendMessage = () => {
  const { state, dispatch } = useAppContext();

  const getCookie = (name: string): string => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop()?.split(";").shift() || "";
    }
    return "";
  };

  const handleSendMessage = async (message: string) => {
    try {
      const newChat: ChatMessage = {
        message,
        created_at: new Date().toISOString(),
      };

      const updatedMessages = [...state.messages, newChat];
      dispatch({ type: "SET_MESSAGES", payload: updatedMessages });
      dispatch({ type: "SET_LOADING", payload: true });
      const csrfToken = getCookie("csrftoken");
      const response = await fetch("http://localhost:8000/ui-chatbot/", {
        method: "POST",
        headers: {
          Accept: "*/*",
          "Accept-Language": "en-US,en;q=0.9,es;q=0.7",
          "Content-Type": "application/x-www-form-urlencoded",
          Origin: "http://localhost:8000",
          Pragma: "no-cache",
          "Cache-Control": "no-cache",
          Referer: "http://localhost:8000/ui-chatbot/",
          "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Site": "same-origin",
          "X-CSRFToken": csrfToken,
        },
        body: `csrfmiddlewaretoken=${encodeURIComponent(
          csrfToken
        )}&message=${encodeURIComponent(message)}`,
        credentials: "include",
      });

      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();

      updatedMessages[updatedMessages.length - 1].response = data.response;
      dispatch({ type: "SET_LOADING", payload: false });
      dispatch({ type: "SET_MESSAGES", payload: updatedMessages });
    } catch (error) {
      console.error("Error posting message:", error);
      dispatch({ type: "SET_LOADING", payload: false });
    }
  };

  return { handleSendMessage };
};

export default useSendMessage;
