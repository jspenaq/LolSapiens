import { configureStore } from "@reduxjs/toolkit";
import leagueClientReducer from "./leagueClientSlice";

const store = configureStore({
  reducer: {
    leagueClient: leagueClientReducer,
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {leagueClient: LeagueClientState}
export type AppDispatch = typeof store.dispatch;

export default store;
