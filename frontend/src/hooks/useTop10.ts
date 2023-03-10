import axios from "axios";
import { useQuery } from "react-query";
import type { UseQueryResult } from "react-query/types/react";
import { BACKEND_BASE, TOP_10 } from "../constants/endpoints";
import type { PickChampionInfo } from "../types";

const getTop10Bans = async (
  lane: string,
  tier: string
): Promise<PickChampionInfo[]> => {
  const { data } = await axios.get<PickChampionInfo[]>(
    `${TOP_10}?${new URLSearchParams({
      lane,
      tier,
    }).toString()}`,
    {
      baseURL: BACKEND_BASE,
    }
  );

  return data;
};

const useTop10 = (
  { lane, tier }: { lane: string; tier: string },
  enabled = true
): UseQueryResult<PickChampionInfo[]> => {
  return useQuery(
    ["top-10-bans", lane, tier],
    getTop10Bans.bind(null, lane, tier),
    {
      enabled,
      initialData: [],
    }
  );
};

export default useTop10;
