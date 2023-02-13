import { useAppDispatch } from "./hooks/reduxHooks";
import { useEffect } from "react";
import { updateClientStatus, updateSummoner } from "./store/leagueClientSlice";
import "./App.scss";
import SapiensRouter from "./SapiensRouter";

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
      {/* TODO: Put the side navigation Here. Check the possibility to use Outlet */}
      <SapiensRouter />
    </>
  );
};

export default App;
