import axios from "axios";
import { useQuery } from "react-query";
import type { UseQueryResult } from "react-query/types/react";
import {
    BACKEND_BASE,
    CHAMPION_KEYSTONES,
} from "../constants/endpoints";
import type { Keystone } from "../types";

export interface ChampionParams {
    champion_id?: string;
    lane?: string;
    tier?: string;
    mode?: string;
    spicy?: string;
}

export interface ChampionKeystones {
    keystones: Keystone[];
}

const getKeystones = async (
    params: ChampionParams | null
): Promise<ChampionKeystones> => {
    const { data } = await axios.get<ChampionKeystones>(
        `${CHAMPION_KEYSTONES}?${new URLSearchParams({ ...params }).toString()}`,
        {
            baseURL: BACKEND_BASE,
        }
    );

    return data;
};

const useKeystones = (
    params: ChampionParams | null,
    enabled = true
): UseQueryResult<ChampionKeystones> => {
    return useQuery(
        ["keystones", params],
        getKeystones.bind(null, params),
        {
            enabled,
        }
    );
};

export default useKeystones;
