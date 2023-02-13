import LCUConnector from "lcu-connector";
import axios from "axios";
import EventEmitter from "events";
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

export interface Credentials {
  username: string;
  password: string;
  address: string;
  port: number;
  protocol: string;
}

enum RiotEndpoints {
  CURRENT_SUMMONER = "/lol-summoner/v1/current-summoner",
}

// El frontend pregunta si existe conexion para almacenar en estado 1re caso \
// Si se desconecta (limpiar credenciales) regresa evento de desconexion. Si se vuelve a conectar regresa evento de conexion 2do caso

export default class LeagueClient {
  private readonly _connector = new LCUConnector();
  private _credentials: Credentials | null = null;
  private _baseUrl: string = "";
  private _authorization: string = "";
  connectorStatus = new EventEmitter();

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
      this.connectorStatus.emit("is-connected", true);
    });

    this._connector.on("disconnect", () => {
      // TODO: Send disconnected event
      console.log("LeagueClient was disconnected");
      this._credentials = null;
      this.connectorStatus.emit("is-connected", false);
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

  async currentSummoner(): Promise<any> {
    try {
      const response: any = await axios(
        `${this._baseUrl}${RiotEndpoints.CURRENT_SUMMONER}`,
        {
          headers: { Authorization: this._authorization },
        }
      );

      return {
        displayName: response.displayName,
        percentCompleteForNextLevel: response.percentCompleteForNextLevel,
        profileIconId: response.profileIconId,
        summonerLevel: response.summonerLevel,
      };
    } catch (error) {
      console.error("Error getting current summoner data");
      console.error(error);
    }
  }
}
