import { DDRAGON_CANISBACK_BASE } from "../../constants/endpoints";
import { useAppSelector } from "../../hooks/reduxHooks";
import type { BuildRunes } from "../../types";
import classes from "./runes.module.scss";

export interface RunesProps {
  runes: BuildRunes;
}

const Runes = ({ runes }: RunesProps): JSX.Element => {
  const runesData = useAppSelector((state) => state.leagueApi.runes_data);
  const primaryRunes = runesData.find(
    (runePath) => runePath.key === runes.primary_path
  );

  console.log(runes);

  return (
    <ul className={classes.runes}>
      {primaryRunes?.slots.map(({ runes = [] }, index) => (
        <li key={index}>
          <ul className={classes.runes__row}>
            {runes.map((rune) => (
              <li key={`slot-${1}:${rune.id}`}>
                <img
                  src={`${DDRAGON_CANISBACK_BASE}/${rune.icon}`}
                  alt={`${rune.key}`}
                />
              </li>
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
};

export default Runes;
