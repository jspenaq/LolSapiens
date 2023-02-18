import { useAppSelector } from "../../hooks/reduxHooks";
import type { BanChampionInfo } from "../../types";
import classes from "./bancard.module.scss";

interface BanCardProps {
  ban: BanChampionInfo;
}

const BanCard = ({ ban }: BanCardProps): JSX.Element => {
  const champions = useAppSelector((state) => state.leagueApi.champions_data);
  const championKeyName = champions?.[`${ban.id}`].key_name ?? "";

  // change for figure and caption maybe
  return (
    <div className={classes.bancard}>
      <img
        src={`http://ddragon.leagueoflegends.com/cdn/img/champion/loading/${championKeyName}_0.jpg`}
        alt="algo"
      />
      <div className={classes.info}>
        <span>Win Rate: {ban.win_rate}</span>
        <span>Pick Rate: {ban.pick_rate}</span>
      </div>
    </div>
  );
};

export default BanCard;
