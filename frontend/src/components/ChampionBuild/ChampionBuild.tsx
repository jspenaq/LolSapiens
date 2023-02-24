import { useAppSelector } from "../../hooks/reduxHooks";
import type { ChampionBuildParams } from "../../hooks/useChampionBuild";
import useChampionBuild from "../../hooks/useChampionBuild";
import classes from "./championbuild.module.scss";
import { useState, useMemo } from "react";
import type { Option } from "../../types";
import { RecommendedBuild, Runes, Select } from "../../components";
import { lanes, modes, spicyList, tiers } from "../../constants";
import type { ActionMeta } from "react-select";

export interface ChampionBuildProps {
  initialQuery?: ChampionBuildParams | null;
  hideGameflowSelects?: boolean;
}

export interface BuildQuery {
  champion: Option | null;
  lane: Option | null;
  tier: Option | null;
  mode: Option | null;
  keystone: Option | null;
  spicy: Option | null;
}

const ChampionBuild = ({
  initialQuery = null,
  hideGameflowSelects = false,
}: ChampionBuildProps): JSX.Element => {
  const championsData = useAppSelector(
    (state) => state.leagueApi.champions_data
  );

  const runesData = useAppSelector((state) => state.leagueApi.runes_data);

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

  const getOptions = (): BuildQuery => {
    return {
      lane:
        lanes.find(
          (lane) =>
            lane.value === initialQuery?.lane || lane.value === "default"
        ) ?? null,
      tier:
        tiers.find(
          (tier) =>
            tier.value === initialQuery?.tier || tier.value === "platinum_plus"
        ) ?? null,
      keystone: { label: "Default", value: "0" },
      spicy:
        spicyList.find(
          (spicy) => spicy.value === initialQuery?.spicy || spicy.value === "0"
        ) ?? null,
      mode:
        modes.find(
          (mode) => mode.value === initialQuery?.mode || mode.value === "ranked"
        ) ?? null,
      // Something happen and the find method doesn't respect the condition order. TODO: check js docs
      champion:
        champions.find(
          (champion) => champion.value === initialQuery?.champion_id?.toString()
        ) ??
        champions.find((champion) => champion.value === "1") ??
        null,
    };
  };

  const [query, setQuery] = useState<BuildQuery>(getOptions);
  const champion = championsData?.[query?.champion?.value as string];

  const handleQueryChange = (
    value: Option | null,
    action: ActionMeta<Option>
  ): void => {
    setQuery((prevState) => {
      const newState: BuildQuery = {
        ...prevState,
        [action.name as string]: value,
      };
      return newState;
    });
  };

  const handleImport = (): void => {
    window.electronApi?.importBuild(data?.build);
  };

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

  const championBuildQuery: ChampionBuildParams = {
    champion_id: query?.champion?.value,
    keystone_id: query?.keystone?.value,
    lane: query?.lane?.value,
    mode: query?.mode?.value,
    spicy: query?.spicy?.value,
    tier: query?.tier?.value,
  };

  const { data } = useChampionBuild(
    championBuildQuery,
    Boolean(championBuildQuery?.champion_id)
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
            name="champion"
            placeholder="Champion"
            value={query?.champion}
          />
        )}
        <Select
          options={lanes}
          onChange={handleQueryChange}
          name="lane"
          placeholder="Lane"
          value={query?.lane}
        />
        <Select
          options={tiers}
          onChange={handleQueryChange}
          name="tier"
          placeholder="Tier"
          value={query?.tier}
        />
        {!hideGameflowSelects && (
          <Select
            options={modes}
            onChange={handleQueryChange}
            name="mode"
            placeholder="Game Mode"
            value={query?.mode}
          />
        )}
        <Select
          options={runes}
          onChange={handleQueryChange}
          name="keystone"
          placeholder="Keystone"
          value={query?.keystone}
        />
        <Select
          options={spicyList}
          onChange={handleQueryChange}
          name="spicy"
          placeholder="Spicy"
          value={query?.spicy}
        />
      </div>
      {champion && (
        <div className={classes.champion}>
          <h2>{champion.name}</h2>
          {champion.title}
          <button onClick={handleImport}>Import Build and Runes</button>
        </div>
      )}
      {data?.runes && <Runes runes={data.runes} />}
      {data?.build && <RecommendedBuild build={data.build} />}
    </div>
  );
};

export default ChampionBuild;
