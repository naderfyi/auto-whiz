import { send } from "process";
import { Styles } from "../../../App";
import { colors } from "../../../ressources/colors";
import SendIcon from "../../../ressources/SendIcon.svg";
import { useState } from "react";
import { MessageType } from "./utils/useHandleChatbotState";
import { handleSendPromptConnect } from "./utils/connect";

type InputFieldProps = {
  setConversationState: React.Dispatch<React.SetStateAction<any>>;
};

export const InputField = (props: InputFieldProps) => {
  const { setConversationState } = props;
  const [prompt, setPrompt] = useState("");

  const handleSendPrompt = async () => {
    setConversationState((prev: MessageType[]) => [
      ...prev,
      { messages: prompt, Sender: "user" },
    ]);
    handleSendPromptConnect(prompt).then((response) => {
      const botResponse = response.response[1];
      setConversationState((prev: MessageType[]) => [
        ...prev,
        { messages: botResponse, Sender: "bot" },
      ]);
    });
    setPrompt("");
  };

  return (
    <div style={styles.container}>
      <input
        style={styles.input}
        placeholder="Type your message here"
        type="text"
        onChange={(e) => setPrompt(e.target.value)}
        onSubmit={handleSendPrompt}
        value={prompt}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSendPrompt();
          }
        }}
      />
      <div style={styles.sendIcon} onClick={handleSendPrompt}>
        <img src={SendIcon} alt="Send" width={24} height={24} />
      </div>
    </div>
  );
};

const styles: Styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
    backgroundColor: colors.white,
    borderRadius: "20px",
    padding: "10px 0",
  },
  input: {
    justifySelf: "flex-end",
    alignSelf: "flex-end",
    width: "80%",
    height: "50px",
    borderRadius: "20px",
    border: "none",
    outline: "none",
    background: "transparent",
    padding: "0 20px",
  },
  sendIcon: {
    display: "flex",
    justifyContent: "flex-end",
    padding: "0 20px",
    alignItems: "center",
    color: colors.greyDark,
    cursor: "pointer",
    width: "20%",
  },
};
