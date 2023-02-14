import React from "react";
import ReactDOM from "react-dom/client";
import "./index.scss";
import store from "./store/store";
import { Provider } from "react-redux";
import { RouterProvider } from "react-router-dom";
import router from "./SapiensRouter";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </React.StrictMode>
);
