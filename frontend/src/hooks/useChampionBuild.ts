import axios from "axios";
import { useQuery } from "react-query";
import type { UseQueryResult } from "react-query/types/react";
import { BACKEND_BASE, CHAMPION_BUILD } from "../constants/endpoints";
import type { Build } from "../types";

export interface ChampionBuildParams {
  champion_id: string;
  lane?: string;
  tier?: string;
  mode?: string;
  keystone_id: string;
  spicy?: string;
}

const getChampionBuild = async (
  params: ChampionBuildParams
): Promise<Build> => {
  const { data } = await axios.get<Build>(
    `${CHAMPION_BUILD}?${new URLSearchParams({ ...params }).toString()}`,
    {
      baseURL: BACKEND_BASE,
    }
  );

  return data;
};

const useChampionBuild = (
  params: ChampionBuildParams,
  enabled = true
): UseQueryResult<Build> => {
  return useQuery(
    ["champion-build", params],
    getChampionBuild.bind(null, params),
    {
      enabled,
    }
  );
};

export default useChampionBuild;
