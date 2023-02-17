import { configureStore } from "@reduxjs/toolkit";
import leagueApiReducer from "./leagueApiSlice";
import leagueClientReducer from "./leagueClientSlice";

const store = configureStore({
  reducer: {
    leagueClient: leagueClientReducer,
    leagueApi: leagueApiReducer,
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {leagueClient: LeagueClientState}
export type AppDispatch = typeof store.dispatch;

export default store;
