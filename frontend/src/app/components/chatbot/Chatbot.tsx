import React, { useState } from "react";
import { Styles } from "../../../App";
import { ChatHeader } from "./ChatHeader";
import { ConversationBox } from "./ConversationBox";
import { useHandleChatbotState } from "./utils/useHandleChatbotState";
import SendIcon from "../../../ressources/SendIcon.svg";  // Import the Send icon

export const Chatbot = () => {
  const [apiKey, setApiKey] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const { conversationState, setConversationState } = useHandleChatbotState();

  const handleApiKeyInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setApiKey(event.target.value);
  };

  const sendApiKeyToServer = async () => {
    const formData = new FormData();
    formData.append('api_key', apiKey);

    try {
        const response = await fetch('http://167.86.120.73:5004/set_api_key', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            setIsAuthenticated(true);
        } else {
            const errorData = await response.json();
            alert(errorData.error || 'Failed to set API key');
        }
    } catch (error) {
        console.error('Failed to fetch:', error);
        alert('Failed to connect to the server. Please check your connection and try again.');
    }
};

  if (!isAuthenticated) {
    return (
      <div style={styles.container}>
        <div style={styles.inputContainer}>
          <input
            style={styles.input}
            type="text"
            value={apiKey}
            onChange={handleApiKeyInput}
            placeholder="Enter your OpenAI API Key"
          />
          <img
            src={SendIcon}
            alt="Set API Key"
            onClick={sendApiKeyToServer}
            style={styles.icon}
          />
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <ChatHeader />
      <ConversationBox
        conversationState={conversationState}
        setConversationState={setConversationState}
      />
    </div>
  );
};

const styles: Styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "space-around",
    padding: "40px",
    height: "80vh",
    borderRadius: "10px",
    backgroundColor: "rgba(47, 45, 45, 0.93)",
    boxShadow: "5px 5px 0px #000",
    width: "550px",
  },
  inputContainer: {
    position: "relative",
    width: "80%",
  },
  input: {
    padding: "10px",
    borderRadius: "5px",
    width: "100%",
    height: "50px",
    border: "none",
    outline: "none",
    background: "#ffffff", // White background
    paddingLeft: "20px",
  },
  icon: {
    position: "absolute",
    top: "50%",
    right: "10px", // Adjust as necessary
    transform: "translateY(-50%)",
    cursor: "pointer",
    width: "24px",
    height: "24px",
  },
};
