import { contextBridge, ipcRenderer, type IpcRendererEvent } from "electron";

contextBridge.exposeInMainWorld("electronApi", {
  importBuild: (data: any) => {
    ipcRenderer.send("import:build", data);
  },
  buildImported: (callback: () => void) =>
    ipcRenderer.on("import:build", callback),
  summonerDetected: (
    callback: (event: IpcRendererEvent, summoner: any) => void
  ) => ipcRenderer.on("summoner:detected", callback),
  clientStatusChange: (
    callback: (event: IpcRendererEvent, isConnected: boolean) => void
  ) => ipcRenderer.on("client-status:change", callback),
  clientStatus: () => {
    ipcRenderer.send("client:status");
  },
  getCurrentSummoner: () => {
    ipcRenderer.send("summoner:get");
  },
  getGameflow: (
    callback: (
      event: IpcRendererEvent,
      gameflow: { gameMode: string; gamePhase: string }
    ) => void
  ) => ipcRenderer.on("gameflow:change", callback),
  getCurrentChampion: (
    callback: (event: IpcRendererEvent, champId: string) => void
  ) => ipcRenderer.on("champ:selected", callback),
  importRunes: (runes: any) => {
    ipcRenderer.send("import:runes", runes);
  },
});
