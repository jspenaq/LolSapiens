import { useAppSelector } from "../../hooks/reduxHooks";
import type { ChampionBuildParams } from "../../hooks/useChampionBuild";
import useChampionBuild from "../../hooks/useChampionBuild";
import classes from "./championbuild.module.scss";
import { useState, useEffect, useMemo } from "react";
import type { Champion, Option } from "../../types";
import { RecommendedBuild, Runes, Select } from "../../components";
import { lanes, modes, spicyList, tiers } from "../../constants";
import type { ActionMeta } from "react-select";

export interface ChampionBuildProps {
  initialQuery?: ChampionBuildParams | null;
  hideGameflowSelects?: boolean;
}

const ChampionBuild = ({
  initialQuery = null,
  hideGameflowSelects = false,
}: ChampionBuildProps): JSX.Element => {
  const championsData = useAppSelector(
    (state) => state.leagueApi.champions_data
  );

  const runesData = useAppSelector((state) => state.leagueApi.runes_data);

  const [champion, setChampion] = useState<Champion>();
  const [query, setQuery] = useState<ChampionBuildParams | null>(initialQuery);

  const handleQueryChange = (
    value: Option | null,
    action: ActionMeta<Option>
  ): void => {
    setQuery((prevState) => {
      const newState: ChampionBuildParams = {
        ...prevState,
        [action.name as string]: value?.value,
      };
      return newState;
    });
  };

  // Better move to redux, same for runes options
  const champions = useMemo<Option[]>(
    () =>
      championsData
        ? Object.values(championsData)
            .map<Option>((champion) => ({
              label: champion.name,
              value: champion.id,
            }))
            .sort((a, b) => a.label.localeCompare(b.label))
        : [],
    [championsData]
  );

  const runes = useMemo<Option[]>(
    () =>
      runesData
        ? Object.values(runesData)
            .map((path) =>
              path.slots[0].runes.map<Option>((rune) => ({
                label: rune.name,
                value: rune.id.toString(),
              }))
            )
            .flat()
            .concat({ label: "Default", value: "0" })
        : [],
    [runesData]
  );

  const defaultValues = useMemo(() => {
    if (initialQuery) {
      return {
        lane: lanes.find((lane) => lane.value === initialQuery.lane),
        tier: tiers.find((tier) => tier.value === initialQuery.tier),
        // keystone_id: .find(y => y.value === initialQuery.y),
        spicy: spicyList.find((spicy) => spicy.value === initialQuery.spicy),
      };
    }
    return null;
  }, [initialQuery]);

  useEffect(() => {
    if (query?.champion_id) {
      setChampion(championsData?.[query.champion_id]);
    }
  }, [championsData, query?.champion_id]);

  const { data: championBuild } = useChampionBuild(
    query,
    Boolean(query?.champion_id) && Boolean(query?.keystone_id)
  );

  if (!championsData) {
    return <></>;
  }

  return (
    <div className={classes["champion-build"]}>
      <div className={classes.controls}>
        {!hideGameflowSelects && (
          <Select
            options={champions}
            onChange={handleQueryChange}
            name="champion_id"
            placeholder="Champion"
          />
        )}
        <Select
          options={lanes}
          onChange={handleQueryChange}
          name="lane"
          placeholder="Lane"
          defaultValue={defaultValues?.lane}
        />
        <Select
          options={tiers}
          onChange={handleQueryChange}
          name="tier"
          placeholder="Tier"
          defaultValue={defaultValues?.tier}
        />
        {!hideGameflowSelects && (
          <Select
            options={modes}
            onChange={handleQueryChange}
            name="mode"
            placeholder="Game Mode"
          />
        )}
        <Select
          options={runes}
          onChange={handleQueryChange}
          name="keystone_id"
          placeholder="Keystone"
        />
        <Select
          options={spicyList}
          onChange={handleQueryChange}
          name="spicy"
          placeholder="Spicy"
          defaultValue={defaultValues?.spicy}
        />
      </div>
      {champion && (
        <div className={classes.champion}>
          <h2>{champion.name}</h2>
          {champion.title}
        </div>
      )}
      <div className={classes.runes}>
        <Runes />
        <Runes />
      </div>
      {championBuild && <RecommendedBuild build={championBuild} />}
    </div>
  );
};

export default ChampionBuild;
