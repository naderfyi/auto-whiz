import { title } from "process";
import { Styles } from "../../../App";
import logo from "../../../ressources/bg_img.jpeg";
import User from "../../../ressources/User.svg";
import { colors } from "../../../ressources/colors";
import { useState } from "react";

const users = [{ name: "User 1" }, { name: "User 2" }, { name: "User 3" }];

export const ChatHeader = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleUserIconClick = () => {
    setIsDropdownOpen(!isDropdownOpen); // Toggle dropdown visibility
  };

  return (
    <div style={styles.outerContainer}>
      <div style={styles.container}>
        <img src={logo} alt="logo" style={styles.logo} />
        <div style={styles.titleContainer}>
          <div style={styles.title}>Auto-Whizz</div>
          <div style={styles.subtitle}>Your Mercedes Digital Assistant.</div>
        </div>
      </div>
      <div
        onClick={handleUserIconClick} // Handle click on user icon
      >
        <img
          src={User}
          alt="user"
          width={96}
          height={96}
          style={styles.user_icon}
        />
      </div>
      {/* Dropdown menu (conditionally rendered based on isDropdownOpen) */}
      {isDropdownOpen && (
        <div style={styles.dropdown}>
          {/* Content of your dropdown menu */}
          <h3>Switch User now</h3>
          {/* Add more options or components as needed */}
          {users.map((user) => (
            <div key={user.name} style={styles.switchUserLink}>
              {user.name}
            </div>
          ))}
        </div>
      )}
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
  user_icon: {
    justifySelf: "flex-end",
    right: "0",
  },
  outerContainer: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    width: "100%",
  },
  dropdown: {
    position: "absolute",
    top: "300px",
    right: "150px",
    backgroundColor: colors.greyLight,
    boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.1)",
    borderRadius: "5px",
    padding: "30px",
  },
  switchUserLink: {
    padding: "10px",
    cursor: "pointer",
  },
};
