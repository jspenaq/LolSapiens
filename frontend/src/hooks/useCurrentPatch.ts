import axios from "axios";
import { useQuery } from "react-query";
import type { UseQueryResult } from "react-query/types/react";
import { DDRAGON_BASE, DDRAGON_VERSIONS } from "../constants/endpoints";

const getCurrentPatch = async (): Promise<string[]> => {
  const { data } = await axios.get<string[]>(DDRAGON_VERSIONS, {
    baseURL: DDRAGON_BASE,
  });

  return data;
};

const useCurrentPatch = (enabled = true): UseQueryResult<string[]> => {
  return useQuery("current-league-parch", getCurrentPatch, {
    enabled,
  });
};

export default useCurrentPatch;
