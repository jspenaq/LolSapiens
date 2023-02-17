import type { PayloadAction } from "@reduxjs/toolkit";
import { createSlice } from "@reduxjs/toolkit";
import type { Gameflow, Summoner } from "../types";

interface LeagueClientState {
  isConnected: boolean;
  summoner: Summoner | null;
  gameflow: Gameflow | null;
  currentChampion: string | null;
}

const TRACK_PHASES = ["Lobby", "Matchmaking", "None"];

const initialState: LeagueClientState = {
  isConnected: false,
  summoner: null,
  gameflow: null,
  currentChampion: null,
};

export const leagueClientSlice = createSlice({
  name: "leagueClient",
  initialState,
  reducers: {
    updateClientStatus: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;

      // remember to reset all data when client is disconnected
      if (!action.payload) {
        state = initialState;
      }
    },
    updateSummoner: (state, action) => {
      state.summoner = action.payload;
    },
    updateGameflow: (state, action: PayloadAction<Gameflow>) => {
      state.gameflow = action.payload;

      if (TRACK_PHASES.includes(action.payload.gamePhase)) {
        state.currentChampion = null;
      }
    },
    updateCurrentChampion: (state, action: PayloadAction<string>) => {
      state.currentChampion = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  updateClientStatus,
  updateSummoner,
  updateCurrentChampion,
  updateGameflow,
} = leagueClientSlice.actions;

export default leagueClientSlice.reducer;
