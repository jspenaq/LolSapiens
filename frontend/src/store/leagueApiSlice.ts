import type { PayloadAction } from "@reduxjs/toolkit";
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { DDRAGON_BASE } from "../constants/endpoints";
import axios from "axios";
import type { InitialData } from "../types";

interface LeagueApiState extends InitialData {
  test: any;
}

const initialState: LeagueApiState = {
  patch: "13.3.1",
  champions: [],
  items: [],
  runes: [],
  test: null,
};

// can be improve whitout blocking code
// export const getInitialData = createAsyncThunk(
//   "leagueClient/getInitialData",
//   async (): Promise<InitialData> => {
//     const { data } = await axios.get<InitialData>("", {
//       baseURL: DDRAGON_BASE,
//     });

//     return data;
//   }
// );

export const leagueApi = createSlice({
  name: "leagueClient",
  initialState,
  reducers: {
    setCurrentPatch: (state, action: PayloadAction<string>) => {
      state.patch = action.payload;
    },
  },
  extraReducers: (builder) => {
    // builder.addCase(getInitialData.fulfilled, (state, action) => {
    //   const { champions, patch } = action.payload;
    //   state.champions = champions;
    //   state.patch = patch;
    // });
  },
});

// Action creators are generated for each case reducer function
export const { setCurrentPatch } = leagueApi.actions;

export default leagueApi.reducer;
