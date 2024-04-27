import React, { CSSProperties } from "react";
import logo from "./logo.svg";
import "./App.css";
import { HomeScreen } from "./app/HomeScreen";

function App() {
  return <HomeScreen />;
}

export type Styles = { [key: string]: CSSProperties };

export default App;
