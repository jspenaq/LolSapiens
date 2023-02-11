import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("electronApi", {
  importBuild: (data: any) => {
    ipcRenderer.send("import:build", data);
  },
});
