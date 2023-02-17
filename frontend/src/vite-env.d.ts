/// <reference types="vite/client" />
/// <reference types="vite-plugin-svgr/client" />

export {};

declare global {
  interface Window {
    electronApi: {
      importBuild: (data: any) => void;
      buildImported: (callback: () => void) => void;
      summonerDetected: (callback: (event: any, summoner: any) => void) => void;
      clientStatusChange: (
        callback: (event: any, isConnected: boolean) => void
      ) => void;
      clientStatus: () => void;
      getCurrentSummoner: () => void;
      getGameflow: (
        callback: (
          event: any,
          gameflow: { gameMode: string; gamePhase: string }
        ) => void
      ) => void;
      getCurrentChampion: (
        callback: (event: any, champId: string) => void
      ) => void;
    };
  }
}
