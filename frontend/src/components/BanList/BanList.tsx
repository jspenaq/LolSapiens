import BanCard from "../../components/BanCard/BanCard";
import type { BanChampionInfo } from "../../types";
import classes from "./banlist.module.scss";

interface BanListProps {
  bans: BanChampionInfo[];
}

const BanList = ({ bans = [] }: BanListProps): JSX.Element => {
  return (
    <ul className={classes.champions}>
      {bans.map((ban) => {
        return (
          <li key={ban.id}>
            <BanCard ban={ban} />
          </li>
        );
      })}
    </ul>
  );
};

export default BanList;
