import "./App.scss";
import {
  createHashRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
  Outlet,
  Navigate,
  useRouteError,
} from "react-router-dom";
import { InfoAndBans } from "./pages";
import { ReactComponent as LolSapiensLogo } from "../public/logo_1.svg";

function ErrorBoundary() {
  let error = useRouteError();
  console.error(error);
  // Uncaught ReferenceError: path is not defined
  return <div>Dang!</div>;
}

const router = createHashRouter(
  createRoutesFromElements(
    <Route
      path="/"
      element={
        <div className="App">
          <hgroup className="App__title">
            <LolSapiensLogo width={72} height={72} />
            <h1>LoL Sapiens</h1>
          </hgroup>
          <Outlet />
        </div>
      }
      errorElement={<ErrorBoundary />}
    >
      <Route path="/info-bans" element={<InfoAndBans />} />
      <Route index element={<Navigate to="/info-bans" />} />
      <Route path="*" element={<Navigate to="/info-bans" />} />
    </Route>
  )
);

function SapiensRouter() {
  return <RouterProvider router={router} />;
}

export default SapiensRouter;
