import {
  createHashRouter,
  createRoutesFromElements,
  Outlet,
  Route,
  useRouteError,
} from "react-router-dom";
import Picks from "./pages/Picks/Picks";
import Navigation from "./components/Navigation/Navigation";
import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "./hooks/reduxHooks";
import { updateClientStatus, updateSummoner } from "./store/leagueClientSlice";
import { getInitialData } from "./store/leagueApiSlice";

function ErrorBoundary(): JSX.Element {
  const error: any = useRouteError();
  console.error(error);
  return <div>{error.message}</div>;
}

const Layout = (): JSX.Element => {
  const champions = useAppSelector((state) => state.leagueApi.champions);

  const dispatch = useAppDispatch();

  useEffect(() => {
    console.log(champions);
  }, [champions]);

  // Set electron handlers
  useEffect(() => {
    // dispatch initaialstate
    dispatch(getInitialData());

    console.log("//Setting electronApi handlers");
    window.electronApi?.clientStatusChange(
      (event: any, isConnected: boolean) => {
        dispatch(updateClientStatus(isConnected));
      }
    );

    window.electronApi?.summonerDetected((event: any, summoner: any) => {
      console.log("setting summoner", summoner);
      dispatch(updateSummoner(summoner));
    });

    // Get current client status
    window.electronApi?.clientStatus();
    return () => {
      window.electronApi?.clientStatusChange(() => {});
      window.electronApi?.summonerDetected(() => {});
    };
  }, []);

  return (
    <>
      <Navigation />
      <main>
        <Outlet />
      </main>
    </>
  );
};

const router = createHashRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />} errorElement={<ErrorBoundary />}>
      {/* <Route index element={Gameflow element} /> */}
      <Route path="picks" element={<Picks />} />
      <Route path="search" element={<Picks />} />
    </Route>
  )
);

export default router;
