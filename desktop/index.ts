import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";
import isDev from "electron-is-dev";
import { type IpcMainEvent } from "electron";
import fs from "fs";

const createWindow = (): void => {
  const mainWindow = new BrowserWindow({
    width: 1024,
    height: 720,
    icon: path.join(
      __dirname,
      process.platform === "darwin"
        ? "assets/logo_darwin.icns"
        : "assets/logo.ico"
    ),
    webPreferences: {
      preload: path.join(__dirname, "preload/electronApi.js"),
    },
  });

  ipcMain.on("import:build", (event: IpcMainEvent, data: any): void => {
    let basePath = "";
    const { championName, build } = data;

    if (process.platform === "darwin") {
      basePath = "/Applications/League of Legends.app/Contents/LoL";
    } else if (process.platform === "win32") {
      basePath = "C:/Riot Games/League of Legends";
    } else {
      return;
    }

    const dir = `${basePath}/Config/Champions/${
      championName as string
    }/Recommended/`;

    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(
      path.join(dir, "build.json"),
      JSON.stringify(build, null, 2)
    );

    mainWindow.webContents.send("import:build")
  });

  if (isDev) {
    mainWindow.loadURL("http://localhost:5173/");
  } else {
    mainWindow.loadFile(path.join(process.resourcesPath, "/dist/index.html"));
  }

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
};

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
