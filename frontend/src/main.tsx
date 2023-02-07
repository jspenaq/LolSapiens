import React from "react";
import ReactDOM from "react-dom/client";
import SapiensRouter from "./SapiensRouter";
import "./index.scss";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <SapiensRouter />
  </React.StrictMode>
);
