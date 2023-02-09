const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronApi", {
  importBuild: (data) => ipcRenderer.send("import:build", data),
});
