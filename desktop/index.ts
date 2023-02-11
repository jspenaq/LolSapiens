// Modules to control application life and create native browser window
import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";
import isDev from "electron-is-dev";
import fs from "fs";
const platform = process.platform;

const createWindow = (): void => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1024,
    height: 720,
    icon: path.join(__dirname, "assets/logo.ico"),
    webPreferences: {
      preload: path.join(__dirname, "preload/electronApi.js"),
    },
  });

  ipcMain.on("import:build", (event, data) => {
    let basePath = "";
    const { championName, build } = data;

    if (platform === "darwin") {
      basePath = "/Applications/League of Legends.app/Contents/LoL";
    } else if (platform === "win32") {
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
  });

  if (isDev) {
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    mainWindow.loadURL("http://localhost:5173/");
  } else {
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    mainWindow.loadFile(path.join(process.resourcesPath, "/dist/index.html"));
  }

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app
  .whenReady()
  .then(() => {
    createWindow();

    app.on("activate", () => {
      // On macOS it's common to re-create a window in the app when the
      // dock icon is clicked and there are no other windows open.
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  })
  .catch(console.log);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
