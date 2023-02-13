import type { PayloadAction } from "@reduxjs/toolkit";
import { createSlice } from "@reduxjs/toolkit";

interface LeagueClientState {
  isConnected: boolean;
  summoner: any;
}

const initialState: LeagueClientState = {
  isConnected: false,
  summoner: null,
};

export const leagueClientSlice = createSlice({
  name: "leagueClient",
  initialState,
  reducers: {
    updateClientStatus: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;
    },
    updateSummoner: (state, action) => {
      state.summoner = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const { updateClientStatus, updateSummoner } = leagueClientSlice.actions;

export default leagueClientSlice.reducer;
