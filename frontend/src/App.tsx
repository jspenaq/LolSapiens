import { useAppDispatch } from "./hooks/reduxHooks";
import { useEffect } from "react";
import { updateClientStatus, updateSummoner } from "./store/leagueClientSlice";
import { Outlet } from "react-router-dom";
import Navigation from "./components/Navigation/Navigation";

const App = (): JSX.Element => {
  const dispatch = useAppDispatch();

  // Set electron handlers
  useEffect(() => {
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

export default App;
