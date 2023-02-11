import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("electronApi", {
  importBuild: (data: any) => {
    ipcRenderer.send("import:build", data);
  },
  buildImported: (callback: () => void) =>
    ipcRenderer.on("import:build", callback),
});
