import BanCard from "../../components/BanCard/BanCard";
import type { PickChampionInfo } from "../../types";
import classes from "./banlist.module.scss";

interface BanListProps {
  bans: PickChampionInfo[];
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
