import {
  createHashRouter,
  createRoutesFromElements,
  Outlet,
  Route,
  useRouteError,
  Navigate,
} from "react-router-dom";
import { Navigation } from "./components";
import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "./hooks/reduxHooks";
import {
  updateClientStatus,
  updateCurrentChampion,
  updateGameflow,
  updateSummoner,
} from "./store/leagueClientSlice";
import { SpicyPicks, Gameflow, Top10, Search } from "./pages";
import { getInitialData } from "./store/leagueApiSlice";

function ErrorBoundary(): JSX.Element {
  const error: any = useRouteError();
  console.error(error);
  return <div>{error.message}</div>;
}

const Layout = (): JSX.Element => {
  const isConnected = useAppSelector((state) => state.leagueClient.isConnected);

  const dispatch = useAppDispatch();

  useEffect(() => {
    if (isConnected) {
      window.electronApi?.getCurrentSummoner();
    }
  }, [isConnected]);

  // Set electron handlers
  useEffect(() => {
    // dispatch initaialstate
    dispatch(getInitialData());

    window.electronApi?.clientStatusChange((_, isConnected) => {
      dispatch(updateClientStatus(isConnected));
    });

    window.electronApi?.summonerDetected((_, summoner) => {
      dispatch(updateSummoner(summoner));
    });

    window.electronApi?.getCurrentChampion((_, champId) => {
      dispatch(updateCurrentChampion(champId.champId));
    });

    window.electronApi?.getGameflow((_, gameflow) => {
      dispatch(updateGameflow(gameflow));
    });

    // Get current client status
    window.electronApi?.clientStatus();
    return () => {
      window.electronApi?.clientStatusChange(() => {});
      window.electronApi?.summonerDetected(() => {});
      window.electronApi?.getCurrentChampion(() => {});
      window.electronApi?.getGameflow(() => {});
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
      <Route index element={<Gameflow />} />
      <Route path="top10" element={<Top10 />} />
      <Route path="spicy" element={<SpicyPicks />} />
      <Route path="search" element={<Search />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Route>
  )
);

export default router;
