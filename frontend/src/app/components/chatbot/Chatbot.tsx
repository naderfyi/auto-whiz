import { Styles } from "../../../App";
import { ChatHeader } from "./ChatHeader";
import { ConversationBox } from "./ConversationBox";
import { useHandleChatbotState } from "./utils/useHandleChatbotState";

export const Chatbot = () => {
  const { conversationState, setConversationState } = useHandleChatbotState();
  const { width } = window.screen;

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
    backgroundColor: "rgba(47 ,45 ,45, 0.93)",
    width: "550px",
  },
};
