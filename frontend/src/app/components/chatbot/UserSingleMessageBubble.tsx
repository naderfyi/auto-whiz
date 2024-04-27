import { Styles } from "../../../App";
import { colors } from "../../../ressources/colors";

export type UserSingleMessageBubbleProps = {
  message: String;
};

export const UserSingleMessageBubble = (
  props: UserSingleMessageBubbleProps
) => {
  return (
    <div
      style={{ ...styles.container, animation: "slideFromLeft 0.5s ease-out" }}
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
    justifyContent: "flex-start",
  },
  innerContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.white,
    padding: "20px 30px 20px 30px",
    borderRadius: "5px 20px 20px 20px",
  },
  message: {
    color: colors.dark,
  },
};
