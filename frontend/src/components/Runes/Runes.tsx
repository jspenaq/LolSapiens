import { DDRAGON_CANISBACK_BASE } from "../../constants/endpoints";
import { useAppSelector } from "../../hooks/reduxHooks";
import type { BuildRunes } from "../../types";
import classes from "./runes.module.scss";
import classNames from "classnames";

export interface RunesProps {
  runes: BuildRunes;
}

const Runes = ({ runes }: RunesProps): JSX.Element => {
  const runesData = useAppSelector((state) => state.leagueApi.runes_data);
  const primaryRunes = runesData.find(
    (runePath) => runePath.key === runes.primary_path
  );

  const secondaryRunes = runesData.find(
    (runePath) => runePath.key === runes.secondary_path
  );

  if (!Object.keys(runes).length) {
    return <></>;
  }

  const activeRunes = runes.primary_path_runes
    .map((rune) => rune.id)
    .concat(runes.secondary_path_runes.map((rune) => rune.id));

  return (
    <div className={classes.runes}>
      <ul>
        {primaryRunes?.slots.map(({ runes = [] }, index) => (
          <li key={index}>
            <ul className={classes.runes__row}>
              {runes.map((rune) => (
                <li key={`slot-${1}:${rune.id}`}>
                  <img
                    src={`${DDRAGON_CANISBACK_BASE}/${rune.icon}`}
                    alt={`${rune.key}`}
                    className={classNames({
                      [classes.active]: activeRunes.includes(
                        rune.id.toString()
                      ),
                    })}
                  />
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>

      <ul>
        {secondaryRunes?.slots.slice(1).map(({ runes = [] }, index) => (
          <li key={index}>
            <ul className={classes.runes__row}>
              {runes.map((rune) => (
                <li key={`slot-${1}:${rune.id}`}>
                  <img
                    src={`${DDRAGON_CANISBACK_BASE}/${rune.icon}`}
                    alt={`${rune.key}`}
                    className={classNames({
                      [classes.active]: activeRunes.includes(
                        rune.id.toString()
                      ),
                    })}
                  />
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Runes;
