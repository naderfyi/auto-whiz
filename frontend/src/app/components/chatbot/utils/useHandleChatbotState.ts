import { useEffect, useState } from "react";

export enum Sender {
  User = "user",
  Bot = "bot",
}

export type MessageType = {
  messages: String;
  Sender: Sender;
};

export const useHandleChatbotState = () => {
  const [conversationState, setConversationState] = useState<
    {
      messages: String;
      Sender: Sender;
    }[]
  >([]);

  const [botResponseLoading, setBotResponseLoading] = useState(false);

  return {
    conversationState,
    setConversationState,
    botResponseLoading,
    setBotResponseLoading,
  };
};
