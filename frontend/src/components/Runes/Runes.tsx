import { DDRAGON_CANISBACK_BASE } from "../../constants/endpoints";
import { useAppSelector } from "../../hooks/reduxHooks";
import classes from "./runes.module.scss";

const Runes = (): JSX.Element => {
  const runes = useAppSelector((state) => state.leagueApi.runes_data);
  const runesBranch = runes[0];

  return (
    <ul className={classes.runes}>
      {runesBranch.slots.map(({ runes = [] }, index) => (
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
