import { app, BrowserWindow } from "electron";
import path from "path";
import isDev from "electron-is-dev";
import LolSapiens from "./LolSapiens";

let mainWindow: LolSapiens;

const createWindow = async (): Promise<void> => {
  mainWindow = new LolSapiens();

  try {
    if (isDev) {
      await mainWindow.loadURL("http://localhost:5173/");
    } else {
      await mainWindow.loadFile(
        path.join(process.resourcesPath, "/dist/index.html")
      );
    }

    // Start connection and subscriptions
    mainWindow.start();
  } catch (e) {
    console.error("Error loading mainWindow", e);
  }
};

app.commandLine.appendSwitch('ignore-certificate-errors')
app
  .whenReady()
  .then(() => {
    createWindow();

    app.on("activate", () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  })
  .catch(console.log);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
