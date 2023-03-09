import axios from "axios";
import { useQuery } from "react-query";
import type { UseQueryResult } from "react-query/types/react";
import {
  BACKEND_BASE,
  CHAMPION_BUILD,
  CHAMPION_RUNES,
} from "../constants/endpoints";
import type { Build, BuildJson, BuildRunes } from "../types";

export interface ChampionBuildParams {
  champion_id?: string;
  lane?: string;
  tier?: string;
  mode?: string;
  keystone_id?: string;
  spicy?: string;
}

export interface ChampionBuild {
  items: BuildJson;
  runes: BuildRunes;
}

const getChampionBuild = async (
  params: ChampionBuildParams | null
): Promise<ChampionBuild> => {
  const { data: build } = await axios.get<Build>(
    `${CHAMPION_BUILD}?${new URLSearchParams({ ...params }).toString()}`,
    {
      baseURL: BACKEND_BASE,
    }
  );

  // const { data: runes } = await axios.get<BuildRunes>(
  //   `${CHAMPION_RUNES}?${new URLSearchParams({ ...params }).toString()}`,
  //   {
  //     baseURL: BACKEND_BASE,
  //   }
  // );
  const runes = build.runes

  const items = build.items
  return { items, runes };
};

const useChampionBuild = (
  params: ChampionBuildParams | null,
  enabled = true
): UseQueryResult<ChampionBuild> => {
  return useQuery(
    ["champion-build", params],
    getChampionBuild.bind(null, params),
    {
      enabled,
    }
  );
};

export default useChampionBuild;
