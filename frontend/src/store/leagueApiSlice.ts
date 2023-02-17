import type { PayloadAction } from "@reduxjs/toolkit";
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { BACKEND_BASE, INITIAL_DATA } from "../constants/endpoints";
import axios from "axios";
import type { Champion, InitialData } from "../types";
import { getChampsByKeyName } from "../utils";

interface LeagueApiState extends InitialData {
  champsByKeyName: Record<string, Champion> | null;
}

const initialState: LeagueApiState = {
  patch: "13.3.1",
  champions_data: null,
  items_data: null,
  runes_data: null,
  champsByKeyName: null,
};

// can be improve whitout blocking code
export const getInitialData = createAsyncThunk(
  "leagueClient/getInitialData",
  async (): Promise<InitialData> => {
    const { data } = await axios.get<InitialData>(INITIAL_DATA, {
      baseURL: BACKEND_BASE,
    });

    return data;
  }
);

export const leagueApi = createSlice({
  name: "leagueClient",
  initialState,
  reducers: {
    setCurrentPatch: (state, action: PayloadAction<string>) => {
      state.patch = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getInitialData.fulfilled, (state, action) => {
      const { champions_data, items_data, patch, runes_data } = action.payload;

      state.champions_data = champions_data;
      state.items_data = items_data;
      state.runes_data = runes_data;
      state.patch = patch;

      // Format and create the aux ChampsByKeyNameMap
      if (action.payload.champions_data) {
        state.champsByKeyName = getChampsByKeyName(
          action.payload.champions_data
        );
      }
    });
  },
});

// Action creators are generated for each case reducer function
export const { setCurrentPatch } = leagueApi.actions;

export default leagueApi.reducer;
