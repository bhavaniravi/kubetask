import { useState } from "react";
import reactLogo from "./assets/react.svg";
import "./App.css";
import SideNavBar from "./SideBar";

var data = {
  title: "kubetask",
  navItems: [{ name: "Jobs" }, { name: "pods" }],
};

function App() {
  return (
    <div className="App">
      <section className="topNavBar"></section>
      <section className="sideNavBar">
        <SideNavBar title={data.title} navItems={data.navItems}></SideNavBar>
      </section>
      <section className="mainSection"></section>
    </div>
  );
}

export default App;
