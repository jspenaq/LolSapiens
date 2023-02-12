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
});
