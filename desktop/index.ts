import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";
import isDev from "electron-is-dev";
import { type IpcMainEvent } from "electron";
import fs from "fs";
import LCUConnector from "lcu-connector";
import got from "got";
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

const connector = new LCUConnector();
let mainWindow: BrowserWindow;

const createWindow = (): void => {
  mainWindow = new BrowserWindow({
    show: false,
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

  if (isDev) {
    mainWindow.loadURL("http://localhost:5173/");
  } else {
    mainWindow.loadFile(path.join(process.resourcesPath, "/dist/index.html"));
  }

  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
    connector.start();
  });

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

  mainWindow.webContents.send("import:build");
});

connector.on("connect", (credentials): void => {
  console.log("connect", credentials);
  const { protocol, address, port, username, password } = credentials;
  const baseUrl = `${protocol}://${address}:${port}`;
  const currenSummonerUrl = `/lol-summoner/v1/current-summoner`;
  const auth = `Basic ${Buffer.from(`${username}:${password}`).toString(
    "base64"
  )}`;

  got
    .get(`${baseUrl}${currenSummonerUrl}`, {
      headers: {
        Authorization: auth,
      },
    })
    .json()
    .then((summoner: any) => {
      const {
        displayName,
        percentCompleteForNextLevel,
        profileIconId,
        summonerLevel,
      } = summoner;
      console.log(summoner);
      mainWindow.webContents.send("summoner:detected", {
        displayName,
        percentCompleteForNextLevel,
        profileIconId,
        summonerLevel,
      });
    });
});
