import { BrowserWindow, ipcMain, type IpcMainEvent } from "electron";
import LeagueClient, { LeagueClientEvents } from "./utils/LeagueClient";
import path from "path";
import fs from "fs";

export default class LolSapiens extends BrowserWindow {
  private readonly _leagueClient = new LeagueClient();

  constructor() {
    super({
      width: 1280,
      height: 720,
      icon: path.join(
        __dirname,
        process.platform === "darwin"
          ? "../assets/logo_darwin.icns"
          : "../assets/logo.ico"
      ),
      webPreferences: {
        preload: path.join(__dirname, "preload/electronApi.js"),
      },
    });
  }

  start(): void {
    // call subscriptions
    this.setImportBuildEvent();
    this.setLeagueClientEvents();
    this.setClientStatusEvent();
    this.setCurrentSummonerEvent();
  }

  setImportBuildEvent(): void {
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

      this.webContents.send("import:build");
    });
  }

  setLeagueClientEvents(): void {
    this._leagueClient.events.on(
      LeagueClientEvents.IS_CONNECTED,
      (isConnected: boolean) => {
        console.log("send connected event from leagueClient :", isConnected);
        this.webContents.send("client-status:change", isConnected);
      }
    );

    this._leagueClient.events.on(
      LeagueClientEvents.CURRENT_SUMMONER,
      (summoner: any) => {
        this.webContents.send("summoner:detected", summoner);
      }
    );
  }

  setClientStatusEvent(): void {
    ipcMain.on("client:status", (event: IpcMainEvent): void => {
      this.webContents.send(
        "client-status:change",
        this._leagueClient.isConnected()
      );
    });
  }

  async setCurrentSummonerEvent(): Promise<void> {
    ipcMain.on("summoner:get", (event: IpcMainEvent) => {
      this._leagueClient.currentSummoner().then((summoner) => {
        this.webContents.send("summoner:detected", summoner);
      });
    });
  }
}
