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
import { useAppDispatch, useAppSelector } from "./hooks/reduxHooks";
import { useEffect } from "react";
import { updateSummoner } from "./store/leagueClientSlice";

function ErrorBoundary(): JSX.Element {
  const error = useRouteError();
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

function SapiensRouter(): JSX.Element {
  const isConnected = useAppSelector((state) => state.leagueClient.isConnected);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (isConnected) {
      console.log("Client connected");
      window.electronApi?.getCurrentSummoner();
    } else {
      console.log("Client disconnected");
      // TODO: Clear all leagueClient data
      dispatch(updateSummoner(null));
    }
  }, [isConnected]);

  return <RouterProvider router={router} />;
}

export default SapiensRouter;
