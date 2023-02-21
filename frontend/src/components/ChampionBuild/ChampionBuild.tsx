import { useAppSelector } from "../../hooks/reduxHooks";
import type { ChampionBuildParams } from "../../hooks/useChampionBuild";
import useChampionBuild from "../../hooks/useChampionBuild";
import classes from "./championbuild.module.scss";
import { useState, useEffect } from "react";
import type { Champion } from "../../types";
import { DDRAGON_BASE, DDRAGON_ITEM } from "../../constants/endpoints";

const ChampionBuild = (): JSX.Element => {
  const patch = useAppSelector((state) => state.leagueApi.patch);
  const runes = useAppSelector((state) => state.leagueApi.runes_data);
  const championsData = useAppSelector(
    (state) => state.leagueApi.champions_data
  );
  const [champion, setChampion] = useState<Champion>();

  useEffect(() => {
    setChampion(championsData?.["1"]);
  }, [championsData]);

  const queryParams: ChampionBuildParams = {
    champion_id: "1",
    keystone_id: "8214",
  };

  const { data: championBuild } = useChampionBuild(
    queryParams,
    Boolean(queryParams.champion_id) && Boolean(queryParams.keystone_id)
  );

  const runesBranch = runes[0];
  console.log(runesBranch);
  console.log(championBuild);
  // const [principals, firstLine, secondLine, thirdLine] = runesBranch.slots;

  if (!championsData || !runes) {
    return <></>;
  }

  return (
    <div className={classes["champion-build"]}>
      <div className={classes.champion}>
        <h2>{champion?.name}</h2>
        {champion?.title}
      </div>
      <div>
        {/* {firstLine.runes.map((rune) => (
          <img key={rune.id} src="" alt={rune.name} />
        ))} */}
      </div>
      <div className={classes.build}>
        <h3>Recommended Build</h3>
        <ul>
          {championBuild?.blocks.map((block, index) => (
            <li key={`${index}-${block.type}`}>
              <p>{block.type}</p>
              <ul className={classes.block__items}>
                {block.items.map((item, index) => (
                  <li key={`${index}-${item.id}`}>
                    <img
                      src={`${DDRAGON_BASE}/cdn/${patch}${DDRAGON_ITEM}/${item.id}.png`}
                      alt={`Item ${item.id} `}
                    />
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ChampionBuild;
