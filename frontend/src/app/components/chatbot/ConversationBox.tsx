import React, { useEffect, useRef } from "react";
import { Styles } from "../../../App";
import { colors } from "../../../ressources/colors";
import { BotSingleMessageBubble } from "./BotSingleMessageBubble";
import { InputField } from "./InputField";
import { UserSingleMessageBubble } from "./UserSingleMessageBubble";
import { MessageType } from "./utils/useHandleChatbotState";

type ConversationBoxProps = {
  conversationState: MessageType[];
  setConversationState: React.Dispatch<React.SetStateAction<any>>;
};

export const ConversationBox = (props: ConversationBoxProps) => {
  const conversationContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Scroll to the bottom smoothly on each conversation state update
    conversationContainerRef.current?.scrollTo({
      top: conversationContainerRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [props.conversationState]);

  return (
    <div style={styles.container}>
      <div ref={conversationContainerRef} style={styles.conversationContainer}>
        {props.conversationState.map((message, index) => {
          return message.Sender === "bot" ? (
            <BotSingleMessageBubble key={index} message={message.messages} />
          ) : (
            <UserSingleMessageBubble key={index} message={message.messages} />
          );
        })}
      </div>
      <div style={styles.inputFieldContainer}>
        <InputField setConversationState={props.setConversationState} />
      </div>
    </div>
  );
};

const styles: Styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "stretch",
    justifyContent: "flex-start",
    backgroundColor: colors.greyLight,
    padding: "40px",
    height: "70%",
    width: "90%",
    borderRadius: "20px",
  },
  conversationContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "stretch",
    justifyContent: "flex-start",
    height: "80%",
    overflowY: "auto",
    gap: "20px",
    msOverflowY: "scroll",
    msOverflowX: "hidden",
  },
  inputFieldContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "stretch",
    justifyContent: "flex-end",
    height: "20%",
  },
};
