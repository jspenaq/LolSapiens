import axios from "axios";
import { useQuery } from "react-query";
import type { UseQueryResult } from "react-query/types/react";
import { BACKEND_BASE, SPICY_PICKS } from "../constants/endpoints";
import type { PickChampionInfo } from "../types";

const getSpicyPicks = async (
  lane: string,
  tier: string
): Promise<PickChampionInfo[]> => {
  const { data } = await axios.get<PickChampionInfo[]>(
    `${SPICY_PICKS}?${new URLSearchParams({
      lane,
      tier,
    }).toString()}`,
    {
      baseURL: BACKEND_BASE,
    }
  );

  return data;
};

const useSpicyPicks = (
  { lane, tier }: { lane: string; tier: string },
  enabled = true
): UseQueryResult<PickChampionInfo[]> => {
  return useQuery(
    ["spicy-picks", lane, tier],
    getSpicyPicks.bind(null, lane, tier),
    {
      enabled,
      initialData: [],
    }
  );
};

export default useSpicyPicks;
