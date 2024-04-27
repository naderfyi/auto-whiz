import { Styles } from "../App";
import bg_img from "../ressources/bg_img.jpeg";
import { Chatbot } from "./components/chatbot/Chatbot";

export const HomeScreen = () => {
  return (
    <div style={styles.container}>
      <img src={bg_img} alt="bg_img" style={styles.bgImage} />
      <Chatbot />
    </div>
  );
};

const styles: Styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    // backgroundColor: "#282c34",
    color: "white",
  },
  bgImage: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    position: "absolute",
    top: 0,
    left: 0,
    zIndex: -1,
  },
};
