import { useAppSelector } from "../../hooks/reduxHooks";
import type { PickChampionInfo } from "../../types";
import classes from "./championloadingcard.module.scss";
import classNames from "classnames";
import {
  DDRAGON_BASE,
  DDRAGON_CHAMPION_LOADING,
} from "../../constants/endpoints";

interface ChampionLoadingCardProps {
  champion: PickChampionInfo;
  isBan?: boolean;
}

const ChampionLoadingCard = ({
  champion,
  isBan = false,
}: ChampionLoadingCardProps): JSX.Element => {
  const champions = useAppSelector((state) => state.leagueApi.champions_data);
  const championKeyName = champions?.[`${champion.id}`].key_name ?? "";

  // change for figure and caption maybe
  return (
    <div
      className={classNames(classes["champion-card"], {
        [classes["is-ban"]]: isBan,
      })}
    >
      <img
        src={`${DDRAGON_BASE}${DDRAGON_CHAMPION_LOADING}/${championKeyName}_0.jpg`}
        alt="algo"
      />
      <div className={classes.info}>
        <span>Win Rate: {champion.win_rate.toFixed(2)}%</span>
        <span>Pick Rate: {champion.pick_rate.toFixed(2)}%</span>
      </div>
    </div>
  );
};

export default ChampionLoadingCard;
