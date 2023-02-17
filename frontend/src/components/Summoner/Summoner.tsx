import { useAppSelector } from "../../hooks/reduxHooks";
import LolSapiensLogo from "../../assets/images/logo.png";
import classes from "./summoner.module.scss";
import { DDRAGON_BASE, DDRAGON_PROFILE_ICON } from "../../constants/endpoints";

const Summoner = (): JSX.Element => {
  const summoner = useAppSelector((state) => state.leagueClient.summoner);
  const patch = useAppSelector((state) => state.leagueApi.patch);

  const iconSrc =
    summoner && patch
      ? `${DDRAGON_BASE}/cdn/${patch}${DDRAGON_PROFILE_ICON}/${summoner.profileIconId}.png`
      : LolSapiensLogo;

  return (
    <div className={classes.summoner}>
      <img src={iconSrc} alt="Summoner profile icon" />
      <h1>{summoner?.displayName ?? "LolSapiens"}</h1>
    </div>
  );
};

export default Summoner;
