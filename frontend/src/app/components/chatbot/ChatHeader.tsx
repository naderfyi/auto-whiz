import { title } from "process";
import { Styles } from "../../../App";
import logo from "../../../ressources/bg_img.jpeg";
import { colors } from "../../../ressources/colors";

export const ChatHeader = () => {
  return (
    <div style={styles.container}>
      <img src={logo} alt="logo" style={styles.logo} />
      <div style={styles.titleContainer}>
        <div style={styles.title}>Auto-Whizz</div>
        <div style={styles.subtitle}>Your Mercedes Digital Assistant.</div>
      </div>
    </div>
  );
};

const styles: Styles = {
  container: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "flex-start",
    gap: "20px",
    width: "100%",
    height: "20%",
    borderTopLeftRadius: "10px",
    borderTopRightRadius: "10px",
  },
  logo: {
    width: "100px",
    height: "100px",
    borderRadius: "50%",
    objectFit: "cover",
  },
  title: {
    fontSize: "1.5rem",
    color: colors.greyDark,
  },
  subtitle: {
    color: colors.greyMedium,
    fontSize: "1rem",
  },
  titleContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    justifyContent: "flex-start",
    gap: "5px",
  },
};
