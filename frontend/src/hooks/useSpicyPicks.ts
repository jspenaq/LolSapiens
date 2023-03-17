import axios from "axios";
import { useQuery } from "react-query";
import type { UseQueryResult } from "react-query/types/react";
import { BACKEND_BASE, SPICY_PICKS } from "../constants/endpoints";
import type { PickChampionInfo } from "../types";

const getSpicyPicks = async (
  lane: string,
  tier: string,
  limit: string
): Promise<PickChampionInfo[]> => {
  const { data } = await axios.get<PickChampionInfo[]>(
    `${SPICY_PICKS}?${new URLSearchParams({
      lane,
      tier,
      limit,
    }).toString()}`,
    {
      baseURL: BACKEND_BASE,
    }
  );

  return data;
};

const useSpicyPicks = (
  { lane, tier, limit }: { lane: string; tier: string; limit: string },
  enabled = true
): UseQueryResult<PickChampionInfo[]> => {
  return useQuery(
    ["spicy-picks", lane, tier, limit],
    getSpicyPicks.bind(null, lane, tier, limit),
    {
      enabled,
      initialData: [],
    }
  );
};

export default useSpicyPicks;
