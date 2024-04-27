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

  useEffect(() => {
    if (
      conversationState.length > 0 &&
      conversationState[conversationState.length - 1].Sender === Sender.User
    ) {
      setBotResponseLoading(true);
      setTimeout(() => {
        setConversationState((prev) => [
          ...prev,
          {
            messages: "I am a bot, I am here to help you",
            Sender: Sender.Bot,
          },
        ]);
      }, 1000);
      setBotResponseLoading(false);
    }
  });
  return {
    conversationState,
    setConversationState,
    botResponseLoading,
  };
};
