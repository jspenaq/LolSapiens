import LCUConnector from "lcu-connector";
import axios from "axios";
import EventEmitter from "events";
import RiotWSProtocol from "./RiotWSProtocol";
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

export interface Credentials {
  username: string;
  password: string;
  address: string;
  port: number;
  protocol: string;
}
const TRACK_PHASES = ["None", "Lobby", "Matchmaking", "ChampSelect"];

enum RiotClientEvents {
  CURRENT_SUMMONER = "OnJsonApiEvent_lol-summoner_v1_current-summoner",
  GAMEFLOW_SESSION = "OnJsonApiEvent_lol-gameflow_v1_session",
  CHAMP_SELECTED = "OnJsonApiEvent_lol-champ-select_v1_current-champion",
}

enum RiotClientEndpoints {
  CURRENT_SUMMONER = "/lol-summoner/v1/current-summoner",
}

export enum LeagueClientEvents {
  IS_CONNECTED = "is-connected",
  CURRENT_SUMMONER = "current-summoner",
  GAMEFLOW_CHANGE = "gameflow-change",
  CHAMP_SELECTED = "champ-selected",
}

const WS_RECONNECT_INTERVAL = 3000;

// El frontend pregunta si existe conexion para almacenar en estado 1re caso \
// Si se desconecta (limpiar credenciales) regresa evento de desconexion. Si se vuelve a conectar regresa evento de conexion 2do caso

export default class LeagueClient {
  private readonly _connector = new LCUConnector();
  private _credentials: Credentials | null = null;
  private _baseUrl: string = "";
  private _authorization: string = "";
  private _ws: RiotWSProtocol | null = null;
  private _wsTimeOutRef: NodeJS.Timeout | null = null;
  events = new EventEmitter();

  constructor() {
    this.initConnector();
  }

  initConnector(): void {
    this._connector.on("connect", (credentials: Credentials) => {
      const { protocol, address, port, username, password } = credentials;
      this._credentials = credentials;
      this._baseUrl = `${protocol}://${address}:${port}`;
      this._authorization = `Basic ${Buffer.from(
        `${username}:${password}`
      ).toString("base64")}`;
      this.events.emit(LeagueClientEvents.IS_CONNECTED, true);
      this.setClientWebSocket(credentials);
    });

    this._connector.on("disconnect", () => {
      // TODO: Send disconnected event
      console.log("LeagueClient disconnected");
      this._credentials = null;
      this.events.emit(LeagueClientEvents.IS_CONNECTED, false);
      this._ws?.close();
    });
    this._connector.start();
  }

  closeConnection(): void {
    console.log("Closing connections");
    this._connector.stop();
    // TODO: close socket connecction
  }

  isConnected(): boolean {
    return Boolean(this._credentials);
  }

  private setClientWebSocket(credentials: Credentials): void {
    this._ws = new RiotWSProtocol(credentials);
    this._ws.on("close", () => {
      console.log("WebSocket Closed");
    });
    this._ws.on("error", (error: any) => {
      console.log("ERROR: ", error.code);
      if (error.code === "ECONNREFUSED") {
        // The ws will close so schedule a new try in x ms
        this._wsTimeOutRef = setTimeout(() => {
          this.setClientWebSocket(credentials);
        }, WS_RECONNECT_INTERVAL);
      }
    });
    this._ws.on("open", () => {
      console.log("WebSocket Opened");
      this.setClientWebSocketSubscriptions();
    });
  }

  private setClientWebSocketSubscriptions(): void {
    if (this._wsTimeOutRef != null) {
      clearTimeout(this._wsTimeOutRef);
      this._wsTimeOutRef = null;
    }
    // Maybe extract this into a function
    // TODO: important remove all listeners/ unsubscribe when ws is closed
    this._ws?.subscribe(RiotClientEvents.CURRENT_SUMMONER, (event: any) => {
      if (event.uri === RiotClientEndpoints.CURRENT_SUMMONER) {
        const summoner = {
          displayName: event.data.displayName,
          percentCompleteForNextLevel: event.data.percentCompleteForNextLevel,
          profileIconId: event.data.profileIconId,
          summonerLevel: event.data.summonerLevel,
        };
        this.events.emit(LeagueClientEvents.CURRENT_SUMMONER, summoner);
      }
    });

    this._ws?.subscribe(RiotClientEvents.GAMEFLOW_SESSION, (event: any) => {
      const gameflow = {
        gameMode: event.data?.map?.gameMode === "ARAM" ? "aram" : "ranked",
        // None, Lobby, Matchmaking, TerminatedInError, WaitingForStats, InProgress, GameStart, ChampSelect, ReadyCheck, PreEndOfGame, EndOfGame
        gamePhase: event.data?.phase,
      };

      if (TRACK_PHASES.includes(gameflow.gamePhase)) {
        this.events.emit(LeagueClientEvents.GAMEFLOW_CHANGE, gameflow);
      }
    });

    this._ws?.subscribe(RiotClientEvents.CHAMP_SELECTED, (event: any) => {
      if (["Create", "Update"].includes(event.eventType)) {
        this.events.emit(LeagueClientEvents.CHAMP_SELECTED, {
          champId: event.data,
        });
      }
    });
  }

  async currentSummoner(): Promise<any> {
    try {
      const response: any = await axios(
        `${this._baseUrl}${RiotClientEndpoints.CURRENT_SUMMONER}`,
        {
          headers: { Authorization: this._authorization },
        }
      );

      return {
        displayName: response.data.displayName,
        percentCompleteForNextLevel: response.data.percentCompleteForNextLevel,
        profileIconId: response.data.profileIconId,
        summonerLevel: response.data.summonerLevel,
      };
    } catch (error: any) {
      // Possible common error error.code === "ECONNREFUSED"
      console.error("Error getting current summoner data");
      if (error.code === "ECONNREFUSED") {
        console.log("ERROR: ", error.code);
      } else {
        throw error;
      }
    }
  }
}
