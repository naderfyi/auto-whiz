import { Styles } from "../../../App";
import { colors } from "../../../ressources/colors";
import "./styles.css";

export type BotSingleMessageBubbleProps = {
  message: String;
};

export const BotSingleMessageBubble = (props: BotSingleMessageBubbleProps) => {
  return (
    <div
      style={{ ...styles.container, animation: "slideFromRight 0.5s ease-out" }}
      className="chatbot-container"
    >
      <div style={styles.innerContainer}>
        <div style={styles.message}>{props.message}</div>
      </div>
    </div>
  );
};

const styles: Styles = {
  container: {
    display: "flex",
    justifyContent: "flex-end",
  },
  innerContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.dark,
    padding: "20px 30px 20px 30px",
    borderRadius: "20px 20px 5px 20px",
  },
  message: {
    color: colors.white,
  },
};
