import React, {
  createContext,
  useContext,
  useReducer,
  ReactNode,
  useEffect,
} from "react";
import { ChatMessage } from "../types";

interface State {
  messages: ChatMessage[];
  isLoading: boolean;
}

const initialState: State = {
  messages: [],
  isLoading: false,
};

type Action =
  | { type: "SET_MESSAGES"; payload: ChatMessage[] }
  | { type: "SET_LOADING"; payload: boolean };

const AppContext = createContext<
  { state: State; dispatch: React.Dispatch<Action> } | undefined
>(undefined);

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "SET_MESSAGES":
      return { ...state, messages: action.payload };
    case "SET_LOADING":
      return { ...state, isLoading: action.payload };
    default:
      return state;
  }
};

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    const chatsDataElement = document.getElementById("chats");
    if (chatsDataElement) {
      try {
        const chatsData: ChatMessage[] = JSON.parse(
          chatsDataElement.textContent || "[]"
        );
        dispatch({ type: "SET_MESSAGES", payload: chatsData });
      } catch (error) {
        console.error("Failed to parse chat data:", error);
      }
    }
  }, []);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error("useAppContext must be used within an AppProvider");
  }
  return context;
};
