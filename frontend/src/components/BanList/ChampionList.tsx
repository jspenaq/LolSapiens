import ChampionLoadingCard from "../ChampionLoadingCard/ChampionLoadingCard";
import type { PickChampionInfo } from "../../types";
import classes from "./championlist.module.scss";

interface ChampionListProps {
  champions: PickChampionInfo[];
  areBan?: boolean;
}

const ChampionList = ({
  champions = [],
  areBan = false,
}: ChampionListProps): JSX.Element => {
  return (
    <ul className={classes.champions}>
      {champions.map((champion) => {
        return (
          <li key={champion.id}>
            <ChampionLoadingCard champion={champion} isBan={areBan} />
          </li>
        );
      })}
    </ul>
  );
};

export default ChampionList;
