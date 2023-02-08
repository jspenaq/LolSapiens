import "./App.scss";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
  Outlet
} from "react-router-dom";
import { InfoAndBans } from "./pages";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route
      path="/"
      element={
        <Outlet />
      }
    >
      <Route path="/info-bans" element={<InfoAndBans/>} />
    </Route>
  )
);

function SapiensRouter() {
  return (
    <div className="App">
      <h1>LoL Sapiens</h1>
      <RouterProvider router={router} />
    </div>
  );
}

export default SapiensRouter;
